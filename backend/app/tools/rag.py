"""RAG tool for querying the active PDF document."""

import logging

from langchain_core.tools import tool

from app.rag.active_window import get_active_pdf
from app.rag.document_manager import get_document_manager
from app.rag.retriever import format_context, retrieve_chunks

logger = logging.getLogger(__name__)


@tool
def query_active_pdf(question: str) -> str:
    """
    Search and answer questions about the PDF currently open in the user's active window.
    Use this when the user asks about 'this PDF', 'this document', a specific page,
    or wants a summary of the open document. Do NOT use for general knowledge questions.
    """
    question = question.strip()
    if not question:
        return "Please ask a question about the PDF."

    pdf_name = get_active_pdf()
    if not pdf_name:
        return (
            "No PDF is currently open in the active window. "
            "Please open a PDF and try again."
        )

    manager = get_document_manager()
    pdf_path, error = manager.resolve_pdf_path(pdf_name)

    if error and not pdf_path:
        return error

    if not pdf_path:
        return f"I couldn't find {pdf_name} on your computer."

    success, msg = manager.ensure_indexed(pdf_path)
    if not success:
        return msg

    try:
        docs = retrieve_chunks(question, file_name=pdf_name)
        if not docs:
            return (
                f"I indexed {pdf_name} but couldn't find relevant content "
                f"for your question. Try rephrasing."
            )

        context = format_context(docs)
        pages = sorted({
            int(d.metadata.get("page", 0)) + 1 for d in docs
        })

        return (
            f"Active PDF: {pdf_name}\n"
            f"Relevant pages: {', '.join(str(p) for p in pages)}\n\n"
            f"Retrieved context:\n{context}\n\n"
            f"Use the above context to answer the user's question: {question}"
        )
    except Exception as exc:
        logger.exception("RAG retrieval failed")
        return f"I had trouble searching the PDF: {exc}"
