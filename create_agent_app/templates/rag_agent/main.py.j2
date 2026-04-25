"""Local CLI entrypoint for RAG agent."""

from __future__ import annotations

from agents.rag_agent import ask_rag_agent
from rag.ingest import ingest_documents


def main() -> None:
    chunks = ingest_documents()
    print(f"Indexed {chunks} chunk(s) from sample_docs.")
    print("RAG CLI ready. Ask about the sample docs. Type 'exit' to quit.")

    while True:
        query = input("\\nQuestion: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("Goodbye")
            break
        if not query:
            continue
        answer = ask_rag_agent(query)
        print(f"\\nAnswer:\n{answer}")


if __name__ == "__main__":
    main()