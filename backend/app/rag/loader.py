import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings


def load_chunk(path: str):
    loader = PyPDFLoader(path)
    pages = loader.load()

    file_name = os.path.basename(path)
    source = os.path.abspath(path)

    for page in pages:
        page.metadata["file_name"] = file_name
        page.metadata["source"] = source
        # PyPDFLoader uses 0-based page numbers; keep for filtering, convert at display time
        if "page" not in page.metadata:
            page.metadata["page"] = 0

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.RAG_CHUNK_SIZE,
        chunk_overlap=settings.RAG_CHUNK_OVERLAP,
    )

    return splitter.split_documents(pages)
