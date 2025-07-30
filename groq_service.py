#!/usr/bin/env python3
"""
Groq LLM Service for query parsing and clause matching
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from loguru import logger
from groq import Groq
from sentence_transformers import SentenceTransformer
import numpy as np

class GroqService:
    """Service for Groq LLM operations."""
    
    def __init__(self):
        """Initialize Groq service."""
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.warning("GROQ_API_KEY not set")
            self.client = None
            return
            
        try:
            self.client = Groq(api_key=self.api_key)
            logger.info("GroqService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Groq: {e}")
            self.client = None
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts using sentence transformers."""
        try:
            # Initialize sentence transformer model
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(texts)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []
    
    async def parse_query(self, query: str) -> Dict[str, Any]:
        """Parse natural language query into structured format."""
        if not self.client:
            return self._fallback_parse_query(query)
        
        try:
            prompt = f"""
            Parse this insurance policy query into structured JSON:
            Query: "{query}"
            
            Return only valid JSON with these fields:
            - intent: the main purpose of the query
            - entities: key terms mentioned
            - conditions: any specific conditions or requirements
            
            Example format:
            {{
                "intent": "find grace period",
                "entities": ["grace period", "premium payment"],
                "conditions": ["after due date"]
            }}
            """
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=200
            )
            
            content = response.choices[0].message.content.strip()
            # Extract JSON from response
            import json
            try:
                # Try to parse as JSON
                result = json.loads(content)
                return result
            except:
                # Fallback parsing
                return self._fallback_parse_query(query)
                
        except Exception as e:
            logger.error(f"Error parsing query: {e}")
            return self._fallback_parse_query(query)
    
    def _fallback_parse_query(self, query: str) -> Dict[str, Any]:
        """Fallback query parser using simple keyword extraction."""
        query_lower = query.lower()
        
        # Enhanced keyword extraction
        keywords = []
        if "grace period" in query_lower:
            keywords.append("grace period")
        if "waiting period" in query_lower:
            keywords.append("waiting period")
        if "premium" in query_lower:
            keywords.append("premium")
        if "coverage" in query_lower:
            keywords.append("coverage")
        if "hospital" in query_lower:
            keywords.append("hospital")
        if "maternity" in query_lower:
            keywords.append("maternity")
        if "claim" in query_lower:
            keywords.append("claim")
        if "ncd" in query_lower or "no claim discount" in query_lower:
            keywords.append("ncd")
        if "deductible" in query_lower:
            keywords.append("deductible")
        if "exclusion" in query_lower:
            keywords.append("exclusion")
        if "benefit" in query_lower:
            keywords.append("benefit")
        if "policy" in query_lower:
            keywords.append("policy")
        if "term" in query_lower:
            keywords.append("term")
        if "renewal" in query_lower:
            keywords.append("renewal")
        if "cancellation" in query_lower:
            keywords.append("cancellation")
        
        # Determine intent
        intent = "general_query"
        if any(word in query_lower for word in ["grace", "waiting"]):
            intent = "find_period"
        elif any(word in query_lower for word in ["premium", "payment"]):
            intent = "find_payment_info"
        elif any(word in query_lower for word in ["coverage", "benefit"]):
            intent = "find_coverage"
        elif any(word in query_lower for word in ["claim", "ncd"]):
            intent = "find_claim_info"
        
        return {
            "intent": intent,
            "entities": keywords,
            "conditions": []
        }
    
    async def evaluate_clause(self, query: str, clause: str) -> Dict[str, Any]:
        """Evaluate if a clause answers the query."""
        if not self.client:
            return self._fallback_evaluate_clause(query, clause)
        
        try:
            prompt = f"""
            Evaluate if this insurance policy clause answers the query:
            
            Query: "{query}"
            Clause: "{clause}"
            
            Return only valid JSON with these fields:
            - answer: "yes" or "no"
            - direct_answer: the specific answer from the clause
            - explanation: why this clause does or doesn't answer the query
            - confidence: 0.0 to 1.0
            
            Example format:
            {{
                "answer": "yes",
                "direct_answer": "Grace period is 30 days",
                "explanation": "Clause directly mentions grace period duration",
                "confidence": 0.9
            }}
            """
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            import json
            try:
                result = json.loads(content)
                return result
            except:
                return self._fallback_evaluate_clause(query, clause)
                
        except Exception as e:
            logger.error(f"Error evaluating clause: {e}")
            return self._fallback_evaluate_clause(query, clause)
    
    def _fallback_evaluate_clause(self, query: str, clause: str) -> Dict[str, Any]:
        """Fallback clause evaluation using simple text matching."""
        query_lower = query.lower()
        clause_lower = clause.lower()
        
        # Simple keyword matching
        query_words = set(query_lower.split())
        clause_words = set(clause_lower.split())
        
        # Calculate overlap
        overlap = len(query_words.intersection(clause_words))
        total_query_words = len(query_words)
        
        if total_query_words == 0:
            confidence = 0.0
        else:
            confidence = min(overlap / total_query_words, 1.0)
        
        # Determine if clause answers query
        if confidence > 0.3:
            answer = "yes"
            direct_answer = clause[:200] + "..." if len(clause) > 200 else clause
            explanation = f"Clause contains {overlap} relevant keywords"
        else:
            answer = "no"
            direct_answer = "No relevant information found"
            explanation = "Clause doesn't contain relevant keywords"
        
        return {
            "answer": answer,
            "direct_answer": direct_answer,
            "explanation": explanation,
            "confidence": confidence
        }
    
    async def generate_detailed_answer(self, query: str, relevant_texts: List[str]) -> str:
        """Generate detailed answer using Groq LLM."""
        if not self.client:
            return self._fallback_generate_answer(query, relevant_texts)
        
        try:
            # Combine relevant texts
            context = "\n\n".join(relevant_texts[:5])  # Limit to 5 texts
            
            prompt = f"""
            Based on this insurance policy information, answer the question:
            
            Question: {query}
            
            Policy Information:
            {context}
            
            Provide a clear, accurate answer based only on the information provided. 
            If the information doesn't contain the answer, say "The policy information doesn't contain specific details about this."
            """
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating detailed answer: {e}")
            return self._fallback_generate_answer(query, relevant_texts)
    
    def _fallback_generate_answer(self, query: str, relevant_texts: List[str]) -> str:
        """Fallback answer generation using simple text processing."""
        if not relevant_texts:
            return "No relevant information found in the document."
        
        # Combine relevant texts
        combined_text = " ".join(relevant_texts)
        
        # Simple answer extraction
        query_lower = query.lower()
        combined_lower = combined_text.lower()
        
        # Find sentences that contain query keywords
        sentences = combined_text.split('.')
        relevant_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(word in sentence_lower for word in query_lower.split()):
                relevant_sentences.append(sentence.strip())
        
        if relevant_sentences:
            answer = ". ".join(relevant_sentences[:3])  # Limit to 3 sentences
            if not answer.endswith('.'):
                answer += "."
        else:
            answer = combined_text[:500] + "..." if len(combined_text) > 500 else combined_text
        
        return answer
    
    async def batch_parse_queries(self, queries: List[str]) -> List[Dict[str, Any]]:
        """Parse multiple queries in batch."""
        return [await self.parse_query(query) for query in queries]
    
    async def batch_evaluate_clauses(self, query: str, clauses: List[str]) -> List[Dict[str, Any]]:
        """Evaluate multiple clauses for a single query."""
        return [await self.evaluate_clause(query, clause) for clause in clauses]
    
    async def batch_generate_answers(self, queries: List[str], relevant_texts_list: List[List[str]]) -> List[str]:
        """Generate answers for multiple queries in batch."""
        answers = []
        for query, relevant_texts in zip(queries, relevant_texts_list):
            answer = await self.generate_detailed_answer(query, relevant_texts)
            answers.append(answer)
        return answers 