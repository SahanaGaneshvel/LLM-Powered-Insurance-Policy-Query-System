import os
from typing import List, Dict, Any
import pdfplumber
import fitz  # PyMuPDF
from docx import Document
import re

# Constants for chunking
CHUNK_SIZE = 500  # tokens (approximate)
CHUNK_OVERLAP = 50  # tokens (approximate)


def extract_text_pdfplumber(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extract text from PDF using pdfplumber.
    Returns a list of dicts with text and page number for each page.
    """
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({"text": text, "page": i + 1})
    return pages

def extract_text_pymupdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extract text from PDF using PyMuPDF (fitz).
    Returns a list of dicts with text and page number for each page.
    """
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text() or ""
        pages.append({"text": text, "page": i + 1})
    return pages

def extract_text_docx(docx_path: str) -> List[Dict[str, Any]]:
    """
    Extract text from DOCX file.
    Returns as a single page (since DOCX has no page info).
    """
    doc = Document(docx_path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return [{"text": full_text, "page": 1}]

def clean_text(text: str) -> str:
    """
    Clean up whitespace and newlines in extracted text.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Split text into overlapping chunks of approximately chunk_size tokens.
    """
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

def process_document(file_path: str) -> List[Dict[str, Any]]:
    """
    Process a single document: extract, clean, chunk, and add metadata.
    Returns a list of chunks with metadata (doc name, page number).
    """
    ext = os.path.splitext(file_path)[1].lower()
    doc_name = os.path.basename(file_path)
    if ext == ".pdf":
        try:
            pages = extract_text_pdfplumber(file_path)
        except Exception:
            pages = extract_text_pymupdf(file_path)
    elif ext == ".docx":
        pages = extract_text_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    chunks_with_meta = []
    for page in pages:
        cleaned = clean_text(page["text"])
        chunks = chunk_text(cleaned)
        for idx, chunk in enumerate(chunks):
            chunks_with_meta.append({
                "text": chunk,
                "doc_name": doc_name,
                "page": page["page"]
            })
    return chunks_with_meta 