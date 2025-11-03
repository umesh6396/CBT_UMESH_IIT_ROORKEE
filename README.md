# A Specialized CBT Therapist AI



### By

* **Name:**Umesh
* **University:** Indian Institute Of Technology,Roorkee
* **Department:** Chemical Engineering


---

## 1. Introduction: From Generalist LLM to a Specialist CBT Therapist

This project investigates and validates the hypothesis that a general-purpose Large Language Model (LLM) can be transformed into a specialized, therapeutically effective Cognitive Behavioral Therapy (CBT) agent through a meticulous process of fine-tuning and advanced architectural design.

Traditional LLMs often lack the domain-specific depth and structured reasoning required for sensitive applications like mental wellness. This project addresses this by developing a robust AI therapist capable of understanding complex emotional states, identifying cognitive distortions, and providing clinically relevant, empathetic, and context-aware CBT-based guidance. This repository documents the end-to-end scientific journey, from initial experimentation and failures to the successful training and evaluation of the "Ultimate CBT Therapist" AI.

## 2. Key Features & Technologies

The project is engineered with a multi-layered architecture to ensure therapeutic efficacy and conversational coherence:

* **Custom Cognitive Engines:**
    * **`EmotionalIntelligenceEngine`:** A rule-based analyzer for multi-dimensional psychological assessment, detecting sentiment, specific emotions (anxiety, depression), cognitive distortions (e.g., catastrophizing, all-or-nothing thinking), and crisis levels.
    * **`CBTResponseStrategyEngine`:** A hierarchical decision-making module that translates analysis into specific therapeutic strategies (e.g., anxiety-focused, cognitive restructuring, crisis intervention).
* **Fine-tuned LLM Core:**
    * Utilizes **`microsoft/phi-2`**, a small yet powerful LLM, fine-tuned using **QLoRA** for stability and efficiency on resource-constrained environments (e.g., Google Colab's free tier GPU).
* **Retrieval-Augmented Generation (RAG):**
    * Integrated **`RAGKnowledgeEngine`** leveraging **ChromaDB** as a vector store for a curated knowledge base of CBT principles and techniques. This mitigates hallucination and grounds responses in factual therapeutic knowledge.
* **Conversational Memory:**
    * Employs a **`collections.deque`** to maintain a sliding window of conversation history, enabling coherent and continuous dialogue.
* **`UltimateGenerationEngine` (Orchestrator):**
    * The central module that orchestrates the entire pipeline: channeling user input through the cognitive engines, retrieving RAG context, composing dynamic prompts, interacting with the fine-tuned LLM, and post-processing responses.
* **User Interface:**
    * A simple and intuitive web-based interface built with **Gradio**, allowing for interactive demonstrations and testing.

## 3. Project Architecture

The system operates through a meticulously designed flow to ensure every interaction is therapeutically structured.

**Flow Description:**
User input from the Gradio UI is first processed by the `UltimateGenerationEngine`. This orchestrator directs the input through the `EmotionalIntelligenceEngine` for psychological analysis, and the `CBTResponseStrategyEngine` to determine the therapeutic approach. Simultaneously, the `RAGKnowledgeEngine` retrieves relevant CBT knowledge. All this information, along with conversation history, is then used to compose a dynamic prompt for the fine-tuned `Phi-2` LLM. The LLM's raw response undergoes post-processing before being displayed as a polished therapeutic response on the Gradio UI.

## 4. Setup and Installation

This project was primarily developed and tested in a Google Colab environment. To replicate the development environment and run the code, it is highly recommended to use Google Colab.




### 4.1. Open and Run the Main Notebook

The primary executable code and development walkthrough are contained within the `source_code_report_Ansh_Attre_IIT_Mandi.ipynb` file.

1.  **Upload to Colab:** Open Google Colab and upload/open the `source_code_report_Ansh_Attre_IIT_Mandi.ipynb`
2.  Add rag_chroma_db and cbt_500.jsonl to your google drive
3.  **Select GPU Runtime:** Ensure you are using a GPU runtime for efficient model loading and inference (Runtime -> Change runtime type -> Hardware accelerator: GPU).
4.  **Run Cells Sequentially:** Execute all cells in the notebook sequentially. This will handle dependency installation, data preparation, model loading, and eventually launch the Gradio UI.

*(**Note:** The `app.py` file is included to demonstrate how the modular components, if fully extracted into `.py` files, would be orchestrated. However, for direct execution and the full development context, the Colab notebook is the intended entry point.)*

### 4.2. Dependencies (Managed by Notebook)

The notebook handles the installation of all necessary Python dependencies (e.g., `torch`, `transformers`, `peft`, `bitsandbytes`, `accelerate`, `chromadb`, `sentence-transformers`, `scikit-learn`, `nltk`, `gradio`, `pandas`, `matplotlib`). The `requirements.txt` file is provided for reference or for setting up a local environment if preferred.

### 4.3. Prepare the CBT Knowledge Base (Managed by Notebook)

The notebook typically includes steps to prepare the RAG knowledge base.

1.  Ensure your CBT-related text documents are in the `knowledge_base/` folder.
2.  The notebook will guide you through initializing ChromaDB using these documents.

### 4.4. Fine-Tune the `microsoft/phi-2` Model (Managed by Notebook)

The `source_code_report_Ansh_Attre_IIT_Mandi.ipynb` file also contains the detailed walkthrough and code for the QLoRA fine-tuning process of the `microsoft/phi-2` model.

## 5. Project Structure

```
.
├── app.py                      # (Demonstrative) Main Gradio application entry point for modular code
├── engines/                    # Contains modular Python code (classes for cognitive engines)
│   ├── emotional_intelligence_engine.py  # Logic for sentiment, emotion, distortion detection
│   ├── cbt_strategy_engine.py          # Logic for therapeutic strategy selection
│   └── rag_knowledge_engine.py         # RAG implementation with ChromaDB (imports database.py)
├── knowledge_base/             # Folder for raw CBT knowledge documents (for RAG)
├── model/                      # Directory for the fine-tuned Phi-2 model checkpoints
├── notebooks/
│   └── source_code_report_Ansh_Attre_IIT_Mandi.ipynb # Detailed development log & primary execution walkthrough
├── scripts/
│   └── create_chromadb.py      # Script to initialize ChromaDB (uses knowledge_base/)
├── prototype_demo_photo_video/ # [Your Demo files]
├── database.py                 # (If this contains ChromaDB specific low-level logic, keep it)
├── cbt_500.jsonl               # Training dataset
├── requirements.txt            # Python dependencies (for reference/local setup)
├── README.md                   # This file
└── .gitignore                  # Git ignore file
```


## 6. Evaluation and Results

The project's performance was evaluated through both qualitative conversational analysis and quantitative metrics, demonstrating effective therapeutic interaction and model stability.



**Thank you for reviewing this project.**
