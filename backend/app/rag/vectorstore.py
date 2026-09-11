from langchain_community.vectorstores import FAISS

from app.rag.embeddings import embedding_model


def create_vector_store(chunks):
    vector_store = FAISS.from_documents(
        chunks,
        embedding_model
    )

    return vector_store