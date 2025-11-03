import chromadb
from chromadb.utils import embeddingfunctions

class RAGKnowledgeEngine:
    def __init__(self, persistpath="ragchromadb", collectionname="cbtknowledge", embeddingmodel="all-MiniLM-L6-v2"):
        self.client = chromadb.PersistentClient(path=persistpath)
        self.embeddingfn = embeddingfunctions.SentenceTransformerEmbeddingFunction(model_name=embeddingmodel)
        self.collection = self.client.get_or_create_collection(
            name=collectionname, embedding_function=self.embeddingfn
        )

    def retrieverelevantknowledge(self, querytext, k=3):
        try:
            results = self.collection.query(query_texts=[querytext], n_results=k)
            return results.get("documents", [])[0]
        except Exception:
            return []
