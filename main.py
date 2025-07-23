from fastapi import FastAPI, Query
from pydantic import BaseModel
from preprocessing.batch_loader import process_all_documents
from embedding.build_index import build_index
from query.semantic_parser import parse_query
from query.clause_retrieval import retrieve_clauses
from llm.groq_llama import get_llm_decision
from feedback.logger import log_query
from feedback.report import generate_weekly_report

app = FastAPI(title="LLM-Powered Policy Query System")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@app.get("/")
def root():
    return {"message": "LLM-Powered Policy Query System is running."}

@app.post("/index")
def index_documents():
    build_index()
    return {"status": "Indexed all policy documents."}

@app.post("/query")
def process_query(request: QueryRequest):
    structured = parse_query(request.query)
    clauses = retrieve_clauses(request.query, top_k=request.top_k)
    decision = get_llm_decision(structured, clauses)
    log_query(request.query, structured, decision)
    return {"structured": structured, "clauses": clauses, "decision": decision}

@app.get("/report")
def get_report():
    report = generate_weekly_report()
    return report 