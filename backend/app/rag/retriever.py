"""RAG retrieval with optional metadata filtering by PDF filename."""

import logging
from typing import Optional

from langchain_core.documents import Document

from app.core.config import settings
from app.rag.vectorstore import load_vector_store

logger = logging.getLogger(__name__)


def _human_page(page_meta) -> int:
    """Convert 0-based page metadata to 1-based human-friendly page number."""
    try:
        return int(page_meta) + 1
    except (TypeError, ValueError):
        return 1


def retrieve_chunks(
    query: str,
    file_name: Optional[str] = None,
    top_k: Optional[int] = None,
) -> list[Document]:
    """
    Retrieve relevant chunks, optionally filtered to a specific PDF.
    """
    k = top_k or settings.RAG_TOP_K
    vector_store = load_vector_store()

    if vector_store is None:
        logger.warning("FAISS index not found")
        return []

    if file_name:
        # Fetch more candidates then filter by metadata
        docs = vector_store.similarity_search(query, k=k * 4)
        filtered = [
            d for d in docs
            if d.metadata.get("file_name", "").lower() == file_name.lower()
        ]
        return filtered[:k]

    return vector_store.similarity_search(query, k=k)


def format_context(docs: list[Document]) -> str:
    """Format retrieved chunks with source metadata for the LLM."""
    if not docs:
        return "No relevant content found in the document."

    parts = []
    for i, doc in enumerate(docs, 1):
        fname = doc.metadata.get("file_name", "unknown")
        page = _human_page(doc.metadata.get("page", 0))
        parts.append(
            f"[Source {i}: {fname}, page {page}]\n{doc.page_content}"
        )

    return "\n\n".join(parts)


def get_retriever(file_name: Optional[str] = None, top_k: Optional[int] = None):
    """Backward-compatible retriever factory with optional file filter."""

    class FilteredRetriever:
        def invoke(self, query: str) -> list[Document]:
            return retrieve_chunks(query, file_name=file_name, top_k=top_k)

        def get_relevant_documents(self, query: str) -> list[Document]:
            return self.invoke(query)

    return FilteredRetriever()
