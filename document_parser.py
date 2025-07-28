import fitz  # PyMuPDF
import docx
import re
import tiktoken
from typing import List, Dict, Any
import aiohttp
import aiofiles
import tempfile
import os
from loguru import logger

class DocumentParser:
    def __init__(self, max_tokens_per_chunk: int = 1000):
        self.max_tokens_per_chunk = max_tokens_per_chunk
        self.tokenizer = tiktoken.get_encoding("cl100k_base")  # OpenAI tokenizer
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using OpenAI tokenizer."""
        return len(self.tokenizer.encode(text))
    
    def split_into_chunks(self, text: str) -> List[str]:
        """Split text into chunks based on token count and logical boundaries."""
        # First split by paragraphs
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        chunks = []
        current_chunk = ""
        current_tokens = 0
        
        for paragraph in paragraphs:
            paragraph_tokens = self.count_tokens(paragraph)
            
            # If adding this paragraph would exceed limit, start new chunk
            if current_tokens + paragraph_tokens > self.max_tokens_per_chunk and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
                current_tokens = paragraph_tokens
            else:
                current_chunk += "\n" + paragraph if current_chunk else paragraph
                current_tokens += paragraph_tokens
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    async def download_document(self, url: str) -> bytes:
        """Download document from URL."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to download document: {response.status}")
                return await response.read()
    
    def parse_pdf(self, file_path: str) -> str:
        """Parse PDF using PyMuPDF for faster processing."""
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            
            doc.close()
            return text
        except Exception as e:
            logger.error(f"Error parsing PDF: {e}")
            raise
    
    def parse_docx(self, file_path: str) -> str:
        """Parse DOCX file."""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            logger.error(f"Error parsing DOCX: {e}")
            raise
    
    def parse_email(self, content: str) -> str:
        """Parse email content (basic implementation)."""
        # Remove email headers
        lines = content.split('\n')
        body_start = 0
        
        for i, line in enumerate(lines):
            if line.strip() == '':
                body_start = i + 1
                break
        
        return '\n'.join(lines[body_start:])
    
    async def process_document_from_url(self, url: str) -> List[Dict[str, Any]]:
        """Process document from URL and return chunks with metadata."""
        # Download document
        content = await self.download_document(url)
        
        # Determine file type
        file_extension = url.split('?')[0].split('.')[-1].lower()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            # Parse based on file type
            if file_extension == 'pdf':
                text = self.parse_pdf(tmp_path)
            elif file_extension in ['docx', 'doc']:
                text = self.parse_docx(tmp_path)
            else:
                # Assume it's email content
                text = self.parse_email(content.decode('utf-8', errors='ignore'))
            
            # Split into chunks
            chunks = self.split_into_chunks(text)
            
            # Create metadata for each chunk
            chunk_metadata = []
            for i, chunk in enumerate(chunks):
                chunk_metadata.append({
                    'text': chunk,
                    'chunk_id': f"chunk_{i}",
                    'doc_source': url,
                    'file_type': file_extension,
                    'token_count': self.count_tokens(chunk),
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                })
            
            return chunk_metadata
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might interfere with processing
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
        return text.strip() 