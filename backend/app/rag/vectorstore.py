import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from pathlib import Path

from langchain_community.vectorstores import FAISS

from app.core.config import settings
from app.rag.embeddings import embedding_model


def get_index_path() -> Path:
    return Path(settings.FAISS_INDEX_DIR)


def create_vector_store(chunks):
    return FAISS.from_documents(chunks, embedding_model)


def load_vector_store() -> FAISS | None:
    index_path = get_index_path()
    if not index_path.exists():
        return None

    return FAISS.load_local(
        str(index_path),
        embedding_model,
        allow_dangerous_deserialization=True,
    )


def save_vector_store(vector_store: FAISS) -> None:
    index_path = get_index_path()
    index_path.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(index_path))
