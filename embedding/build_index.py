import os
from preprocessing.batch_loader import process_all_documents
from .embedding_index import EmbeddingIndexer

POLICY_DIR = os.path.join(os.path.dirname(__file__), '../data/policies')

def build_index():
    chunks = process_all_documents(POLICY_DIR)
    indexer = EmbeddingIndexer()
    indexer.add(chunks)
    print(f"Indexed {len(chunks)} chunks from policy documents.")

if __name__ == "__main__":
    build_index() 