"""PDF path resolution — delegates to document manager."""

from app.rag.document_manager import get_document_manager


def find_pdf_path(filename: str) -> str | None:
    manager = get_document_manager()
    path, _error = manager.resolve_pdf_path(filename)
    return path
