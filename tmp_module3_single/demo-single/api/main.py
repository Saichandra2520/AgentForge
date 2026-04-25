"""FastAPI entrypoint for invoking the generated LangGraph agent."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from agents.agent import invoke_agent

app = FastAPI(title="demo-single API")


class InvokeRequest(BaseModel):
    query: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/invoke")
def invoke(payload: InvokeRequest) -> dict[str, str]:
    answer = invoke_agent(payload.query)
    return {"answer": answer}