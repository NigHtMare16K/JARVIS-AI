"""Incremental PDF ingestion into FAISS."""

import logging

from app.rag.loader import load_chunk
from app.rag.vectorstore import create_vector_store, load_vector_store, save_vector_store

logger = logging.getLogger(__name__)


def _remove_file_chunks(vector_store, file_name: str) -> None:
    """Remove all chunks belonging to a given PDF filename."""
    ids_to_delete = []
    docstore = vector_store.docstore

    for doc_id in vector_store.index_to_docstore_id.values():
        doc = docstore.search(doc_id)
        if doc and doc.metadata.get("file_name", "").lower() == file_name.lower():
            ids_to_delete.append(doc_id)

    if ids_to_delete:
        vector_store.delete(ids_to_delete)
        logger.info("Removed %d old chunks for %s", len(ids_to_delete), file_name)


def ingest_pdf(pdf_path: str) -> int:
    """
    Ingest a PDF into the FAISS index.
    Re-indexes if the file already exists in the index.
    Returns number of chunks added.
    """
    chunks = load_chunk(pdf_path)
    if not chunks:
        logger.warning("No chunks created for %s", pdf_path)
        return 0

    file_name = chunks[0].metadata.get("file_name", "")

    existing = load_vector_store()
    if existing:
        _remove_file_chunks(existing, file_name)
        existing.add_documents(chunks)
        save_vector_store(existing)
    else:
        vector_store = create_vector_store(chunks)
        save_vector_store(vector_store)

    logger.info("Ingested %d chunks from %s", len(chunks), file_name)
    return len(chunks)
