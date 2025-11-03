# therapist_engine.py

import torch
import re
import random
from collections import deque
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import chromadb
from chromadb.utils import embedding_functions

# NOTE: This file contains all the custom classes that form the "brain" of the therapist AI.

# === Class 1: Emotional Intelligence Engine ===
class EmotionalIntelligenceEngine:
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.emotion_patterns = {
            'anxiety': {'keywords': ['worried', 'anxious', 'scared', 'panic', 'nervous', 'fear', 'stress']},
            'depression': {'keywords': ['sad', 'hopeless', 'empty', 'worthless', 'tired', 'meaningless']},
            'anger': {'keywords': ['angry', 'frustrated', 'furious', 'annoyed', 'irritated', 'rage']},
            'grief': {'keywords': ['loss', 'died', 'miss', 'gone', 'funeral', 'bereaved']},
            'trauma': {'keywords': ['flashback', 'nightmare', 'triggered', 'ptsd', 'abuse', 'accident']},
            'relationships': {'keywords': ['relationship', 'partner', 'marriage', 'divorce', 'breakup', 'lonely']}
        }
        self.cognitive_distortions = {
            'all_or_nothing': ['always', 'never', 'completely', 'totally', 'everything', 'nothing'],
            'catastrophizing': ['disaster', 'terrible', 'awful', 'end of world', 'ruined'],
            'mind_reading': ['they think', 'everyone believes', 'people assume'],
            'fortune_telling': ['will never', 'going to fail', "won't work", 'bound to'],
            'emotional_reasoning': ['feel like', 'seems like', 'must be because I feel'],
            'should_statements': ['should', 'must', 'ought to', 'have to'],
            'labeling': ["I am", "he is", "she is"] + ['stupid', 'failure', 'loser', 'worthless'],
            'personalization': ["my fault", "because of me", "I caused", "I'm responsible"]
        }

    def analyze_emotional_state(self, text):
        text_lower = text.lower()
        sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
        detected_emotions = [e for e, p in self.emotion_patterns.items() if any(k in text_lower for k in p['keywords'])]
        detected_distortions = [d for d, p in self.cognitive_distortions.items() if any(k in text_lower for k in p)]
        crisis_keywords = ['suicide', 'kill myself', 'end it all', 'want to die', 'hurt myself', 'self harm']
        crisis_level = 'high' if any(k in text_lower for k in crisis_keywords) else 'low'
        return {
            'primary_emotions': detected_emotions[:2],
            'sentiment': sentiment_scores,
            'cognitive_distortions': detected_distortions,
            'crisis_level': crisis_level
        }

# === Class 2: CBT Response Strategy Engine ===
class CBTResponseStrategyEngine:
    def __init__(self):
        self.therapy_approaches = {
            'crisis_intervention': {'priority': 'immediate safety', 'tone': 'calm, directive'},
            'anxiety_focused': {'priority': 'worry reduction', 'tone': 'gentle, reassuring'},
            'depression_focused': {'priority': 'behavioral activation', 'tone': 'warm, encouraging'},
            'trauma_informed': {'priority': 'safety and stabilization', 'tone': 'careful, validating'},
            'relationship_focused': {'priority': 'communication skills', 'tone': 'balanced, insightful'},
            'cognitive_restructuring': {'priority': 'challenging thoughts', 'tone': 'collaborative, curious'}
        }

    def select_strategy(self, emotional_analysis):
        if emotional_analysis['crisis_level'] == 'high': return 'crisis_intervention'
        if emotional_analysis['primary_emotions']:
            primary = emotional_analysis['primary_emotions'][0]
            if primary == 'trauma': return 'trauma_informed'
            if primary == 'anxiety': return 'anxiety_focused'
            if primary == 'depression': return 'depression_focused'
            if primary == 'relationships': return 'relationship_focused'
        if emotional_analysis['cognitive_distortions']: return 'cognitive_restructuring'
        return 'cognitive_restructuring'

# === Class 3: RAG Knowledge Engine ===
class RAGKnowledgeEngine:
    def __init__(self, persist_path="rag_chroma_db", collection_name="cbt_knowledge"):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(name=collection_name, embedding_function=self.embedding_fn)

    def retrieve_relevant_knowledge(self, query_text, k=3):
        try:
            results = self.collection.query(query_texts=[query_text], n_results=k)
            return results.get("documents", [[]])[0]
        except Exception:
            return []

# === Class 4: Ultimate Generation Engine (The Main Orchestrator) ===
class UltimateGenerationEngine:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.ei_engine = EmotionalIntelligenceEngine()
        self.strategy_engine = CBTResponseStrategyEngine()
        self.rag_engine = RAGKnowledgeEngine()
        self.conversation_memory = deque(maxlen=6)

    def _format_rag_knowledge(self, docs):
        if not docs: return ""
        snippets = [f"- {doc.strip()}" for doc in docs]
        return "Relevant Knowledge (use if helpful, otherwise ignore):\n" + "\n".join(snippets) + "\n"

    def post_process_response(self, response):
        stop_tokens = ["<|", "</", "[/", "User:", "Therapist:", "###"]
        for token in stop_tokens:
            if token in response:
                response = response.split(token)[0].strip()
        sentences = re.split(r'(?<=[.!?])\s+', response)
        clean_sentences = [s.strip().capitalize() for s in sentences if s.strip()]
        response = ' '.join(clean_sentences)
        if not response:
            return "I'm not sure how to respond to that. Could you please tell me more?"
        collaborative_markers = ['what', 'how', 'would you', 'can we', 'together']
        if len(response.split()) > 25 and not any(m in response.lower() for m in collaborative_markers):
            response += f" {random.choice(['How does that sound to you?', 'What are your thoughts on this?'])}"
        return response

    def generate_master_response(self, user_input):
        analysis = self.ei_engine.analyze_emotional_state(user_input)
        strategy = self.strategy_engine.select_strategy(analysis)
        
        history = "".join(f"User: {turn['user']}\nTherapist: {turn['assistant']}\n\n" for turn in self.conversation_memory)
        
        rag_docs = self.rag_engine.retrieve_relevant_knowledge(user_input)
        rag_context = self._format_rag_knowledge(rag_docs)

        prompt = f"""You are a supportive CBT therapist. Continue the conversation naturally based on the user's message.
{rag_context}{history}User: {user_input}
Therapist:"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs, max_new_tokens=250, min_new_tokens=50, do_sample=True,
                temperature=0.7, top_p=0.95, repetition_penalty=1.15,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        raw_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        generated_text = raw_response.split("Therapist:")[-1].strip()
        polished_response = self.post_process_response(generated_text)
        
        self.conversation_memory.append({'user': user_input, 'assistant': polished_response})
        
        # Return the response and the analysis for logging/debugging
        return polished_response, analysis, strategy
