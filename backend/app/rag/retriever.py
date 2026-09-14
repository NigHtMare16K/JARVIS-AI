from langchain_community.vector_stores import FAISS
from app.rag.embeddings import embedding_model

def get_retriever():

    vector_store = FAISS.load_local(
        "faiss_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    return retriever