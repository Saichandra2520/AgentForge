"""FastAPI app for the generated RAG agent."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from agents.rag_agent import ask_rag_agent
from rag.ingest import ingest_documents

app = FastAPI(title="demo-rag API")


class InvokeRequest(BaseModel):
    query: str


@app.on_event("startup")
def startup() -> None:
    ingest_documents()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/invoke")
def invoke(payload: InvokeRequest) -> dict[str, str]:
    answer = ask_rag_agent(payload.query)
    return {"answer": answer}