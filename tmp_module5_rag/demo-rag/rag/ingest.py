"""Ingest local documents into Chroma for retrieval."""

from __future__ import annotations

from pathlib import Path

from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.vectorstore import get_vectorstore


def ingest_documents(docs_dir: Path | None = None) -> int:
    target_dir = docs_dir or (Path(__file__).resolve().parent.parent / "sample_docs")
    if not target_dir.exists():
        return 0

    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=120)
    docs: list[Document] = []

    for path in sorted(target_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        chunks = splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            docs.append(
                Document(
                    page_content=chunk,
                    metadata={"source": path.name, "chunk": i},
                )
            )

    if not docs:
        return 0

    store = get_vectorstore()
    store.add_documents(docs)
    return len(docs)