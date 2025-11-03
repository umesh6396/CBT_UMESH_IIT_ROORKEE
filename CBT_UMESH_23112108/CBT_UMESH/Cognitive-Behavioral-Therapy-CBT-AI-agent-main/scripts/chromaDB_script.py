import os
import glob
import chromadb
from chromadb.utils import embedding_functions

# Folder where your scraped knowledge files are stored
KB_FOLDER = "knowledge_base"

# Create Chroma client (local persistent DB)
client = chromadb.PersistentClient(path="rag_chroma_db")

# Create / get a collection with embedding function
collection = client.get_or_create_collection(
    name="cbt_knowledge",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)

# Step 1: Load all text files from knowledge_base/
def load_files(folder):
    docs = []
    for file in glob.glob(os.path.join(folder, "*.txt")):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
            docs.append((os.path.basename(file), text))
    return docs

# Step 2: Chunk text into smaller pieces
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

# Step 3: Add documents into ChromaDB
def add_to_chromadb():
    docs = load_files(KB_FOLDER)
    for doc_name, text in docs:
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                ids=[f"{doc_name}_{i}"],
                metadatas=[{"source": doc_name}]
            )
    print("✅ Knowledge base added to ChromaDB")

# Step 4: Query the knowledge base
def query_chromadb(query, top_k=3):
    results = collection.query(query_texts=[query], n_results=top_k)
    for i in range(len(results["documents"][0])):
        print(f"\n📖 Result {i+1} (from {results['metadatas'][0][i]['source']}):")
        print(results["documents"][0][i])

# ---- RUN ----
if __name__ == "__main__":
    add_to_chromadb()

    # Example query
    query_chromadb("What is CBT and how does it help with anxiety?")
