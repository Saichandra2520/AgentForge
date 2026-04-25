"""LangChain tool wrapper for retrieval."""

from __future__ import annotations

from langchain_core.tools import tool

from rag.retriever import retrieve_context


@tool
def retrieve_knowledge(query: str) -> str:
    """Fetch the most relevant chunks from the local Chroma vector store."""
    chunks = retrieve_context(query, k=4)
    if not chunks:
        return "No relevant context found in vector store."

    joined = "\n\n---\n\n".join(chunks)
    return f"Retrieved context:\n{joined}"