from embedding.embedding_index import EmbeddingIndexer
from typing import List, Dict

def retrieve_clauses(query: str, top_k: int = 5) -> List[Dict]:
    indexer = EmbeddingIndexer()
    results = indexer.search(query, top_k=top_k)
    return results 