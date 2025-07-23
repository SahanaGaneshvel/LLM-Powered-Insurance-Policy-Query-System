import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

EMBEDDING_MODEL = 'all-MiniLM-L6-v2'  # You can change to a Groq-compatible model if needed
INDEX_PATH = 'faiss_index.bin'
META_PATH = 'faiss_meta.pkl'

class EmbeddingIndexer:
    def __init__(self, embedding_model: str = EMBEDDING_MODEL):
        self.model = SentenceTransformer(embedding_model)
        self.index = None
        self.metadata = []
        self.dim = self.model.get_sentence_embedding_dimension()
        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            self.load()
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.metadata = []

    def embed(self, texts: List[str]):
        return self.model.encode(texts, show_progress_bar=True)

    def add(self, chunks: List[Dict[str, Any]]):
        texts = [c['text'] for c in chunks]
        embeddings = self.embed(texts)
        self.index.add(embeddings)
        self.metadata.extend([{k: v for k, v in c.items() if k != 'text'} for c in chunks])
        self.save()

    def search(self, query: str, top_k: int = 5):
        q_emb = self.embed([query])
        D, I = self.index.search(q_emb, top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results

    def save(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, 'wb') as f:
            pickle.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, 'rb') as f:
            self.metadata = pickle.load(f) 