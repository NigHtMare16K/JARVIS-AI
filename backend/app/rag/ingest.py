from app.rag.loader import load_chunk
from app.rag.vectorstore import create_vector_store


def ingest_pdf(pdf_path: str):

    # 1. Load and split PDF
    chunks = load_chunk(pdf_path)

    print(f"📄 Created {len(chunks)} chunks")

    # 2. Create FAISS vector store
    vector_store = create_vector_store(chunks)

    # 3. Save locally
    vector_store.save_local("faiss_index")

    print("✅ FAISS index created and saved")


if __name__ == "__main__":

    pdf_path = input("Enter PDF path: ")

    ingest_pdf(pdf_path)