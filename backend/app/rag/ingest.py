print("🔥 INGEST FILE LOADED")

from app.rag.loader import load_chunk

print("✅ loader imported")

from app.rag.vectorstore import create_vector_store

print("✅ vectorstore imported")

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

    print("🚀 Starting ingestion...")

    pdf_path = "C:/Users/ASHUTOSH/Downloads/Ashutosh_Kumar_Resume_UPL_NextGenIntern.pdf"

    ingest_pdf(pdf_path)