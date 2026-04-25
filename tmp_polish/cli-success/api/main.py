"""FastAPI app for the multi-agent supervisor workflow."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from agents.supervisor import run_supervisor_workflow

app = FastAPI(title="cli-success API")


class InvokeRequest(BaseModel):
    task: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/invoke")
def invoke(payload: InvokeRequest) -> dict[str, str]:
    answer = run_supervisor_workflow(payload.task)
    return {"answer": answer}