import os
import openai
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
GROQ_API_BASE = "https://api.groq.com/openai/v1/"

openai.api_key = GROQ_API_KEY
openai.base_url = GROQ_API_BASE

def build_prompt(structured_query: Dict, clauses: List[Dict]) -> str:
    prompt = f"""
 
{{
  "decision": "approved/rejected",
  "amount": "if applicable",
  "justification": "explanation in plain English",
  "references": ["doc_name - Clause page"]
}}

Structured Query: {structured_query}
Relevant Clauses:
"""
    for c in clauses:
        prompt += f"\n- {c['doc_name']} (Page {c['page']}): {c.get('text', '')[:200]}..."
    prompt += "\nRespond only with the JSON."
    return prompt

def get_llm_decision(structured_query: Dict, clauses: List[Dict]) -> Dict:
    prompt = build_prompt(structured_query, clauses)
    response = openai.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=512
    )
    # Extract JSON from LLM response
    import json
    import re
    text = response.choices[0].message.content
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return {"error": "Could not parse LLM response", "raw": text} 