"""Search tool used by the researcher worker."""

from __future__ import annotations

from langchain_core.tools import tool


@tool
def search_web(query: str) -> str:
    """Return a lightweight simulated web-search summary for a topic."""
    query_lower = query.lower()

    if "langgraph" in query_lower:
        return (
            "LangGraph is a framework for stateful, controllable agent workflows. "
            "It supports graph-based orchestration, tool usage, and durable execution patterns."
        )

    if "groq" in query_lower:
        return (
            "Groq provides fast inference for open models. Typical setup uses a GROQ_API_KEY "
            "and model names such as llama-3.3-70b-versatile."
        )

    return (
        "No specific indexed summary for this query. Use this as a placeholder note: "
        f"{query.strip()}"
    )