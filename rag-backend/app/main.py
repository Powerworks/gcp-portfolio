from fastapi import FastAPI, HTTPException, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import os
from app.engine import rag_engine

app = FastAPI(title="William Power | Portfolio RAG API", version="1.0.0")

# Enforce explicit CORS filtering so malicious client targets cannot hijack compute
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://axiomatic-spark-505611-t0.web.app", "http://localhost:4321"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    prompt: str

class QueryResponse(BaseModel):
    answer: str

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy", "service": "portfolio-rag-backend"}

@app.post("/api/v1/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt context cannot be empty.")
    
    try:
        # Dispatch query to your LlamaIndex pipeline
        result = rag_engine.query(request.prompt)
        return QueryResponse(answer=result)
    except Exception as e:
        # Graceful error isolation preventing full trace leaks
        raise HTTPException(status_code=500, detail="Internal RAG execution engine failure.")