import os
from .pipeline import process_document
from typing import List, Dict, Any

def process_all_documents(directory: str) -> List[Dict[str, Any]]:
    """Process all .pdf and .docx files in the directory, return all chunks with metadata."""
    all_chunks = []
    for fname in os.listdir(directory):
        if fname.lower().endswith(('.pdf', '.docx')):
            fpath = os.path.join(directory, fname)
            chunks = process_document(fpath)
            all_chunks.extend(chunks)
    return all_chunks 