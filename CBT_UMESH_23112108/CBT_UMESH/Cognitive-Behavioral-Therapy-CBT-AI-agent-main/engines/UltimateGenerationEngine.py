class UltimateGenerationEngine:
    def __init__(self, model, tokenizer): # Corrected __init__ method
        self.model = model
        self.tokenizer = tokenizer

        # Make sure to initialize these if they are not globally available
        self.ei_engine = EmotionalIntelligenceEngine()
        self.strategy_engine = CBTResponseStrategyEngine()
        self.conversation_memory = deque(maxlen=10)

        # RAG ADDITION: initialize RAG
        self.rag_engine = RAGKnowledgeEngine() # Using the renamed class
        self.rag_top_k = 4

    def _format_rag_knowledge(self, docs):
        if not docs:
            return ""
        snippets = []
        for d in docs:
            if not d or 'content' not in d: # Check if doc is valid and has 'content'
                continue
            # safe limit per document to keep prompt under control
            snippet = d['content'].strip().replace("\n", " ")
            if len(snippet) > 600:
                snippet = snippet[:600] + "..."
            snippets.append(f"- {snippet}")
        if not snippets:
            return ""
        return "Relevant Knowledge (use if helpful, otherwise ignore):\n" + "\n".join(snippets) + "\n"


    def post_process_response(self, response):
        """
        This is the POLISHING function. It cleans the raw output from the model.
        """
        # Step 1: Get the core response by splitting at the first sign of an artifact
        stop_tokens = ["<|", "</", "[/", "<&", "User:", "Therapist:", "CLINICAL ASSESSMENT", "QUALITY VERIFICATION", "###"]
        for token in stop_tokens:
            if token in response:
                response = response.split(token)[0].strip()

        # Step 2: Handle sentence structure and capitalization
        sentences = re.split(r'(?<=[.!?])\s+', response)
        clean_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                if not sentence[0].isupper():
                    sentence = sentence[0].upper() + sentence[1:]
                clean_sentences.append(sentence)
        response = ' '.join(clean_sentences)

        if not response:
            return "I'm not sure how to respond to that. Could you please tell me more?"

        # Step 3: Add a collaborative ending if missing
        collaborative_markers = ['what', 'how', 'would you', 'can we', 'together']
        if len(response.split()) > 25 and not any(marker in response.lower() for marker in collaborative_markers):
            endings = [ "How does that sound to you?", "What are your thoughts on this?" ]
            response += f" {random.choice(endings)}"

        return response

    def generate_master_response(self, user_input):
        """
        CHANGED: This function now uses conversation memory to provide context.
        REASON: To create more natural, flowing conversations where the agent
        remembers what was said before.
        """
        analysis = self.ei_engine.analyze_emotional_state(user_input)
        strategy = self.strategy_engine.select_strategy(analysis)

        # --- START OF NEW MEMORY LOGIC ---
        # 1. Build the conversation history from memory
        history = ""
        for turn in self.conversation_memory:
            history += f"User: {turn.get('user', '')}\nTherapist: {turn.get('assistant', '')}\n\n"

        # RAG ADDITION: get relevant knowledge from your Chroma DB
        rag_docs = self.rag_engine.retrieve_relevant_knowledge(user_input, k=self.rag_top_k) # Using the renamed method
        rag_context = self._format_rag_knowledge(rag_docs)

        # 2. Create the prompt with the history included + RAG context
        prompt = f"""You are a supportive CBT therapist. Continue the conversation naturally.
{rag_context}{history}User: {user_input}
Therapist:"""

        # --- END OF NEW MEMORY LOGIC ---
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=250,
                min_new_tokens=70,
                do_sample=True,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.2,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        raw_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract the part after the LAST "Therapist:"
        if "Therapist:" in raw_response:
            generated_text = raw_response.split("Therapist:")[-1].strip()
        else:
            generated_text = raw_response.replace(prompt.replace("Therapist:", ""), "").strip()

        # Polishing the response
        polished_response = self.post_process_response(generated_text)

        # Add the current turn to memory
        self.conversation_memory.append({'user': user_input, 'assistant': polished_response})

        return polished_response, analysis, strategy
