import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_chunk(path: str):
    loader = PyPDFLoader(path)
    pages = loader.load()

    file_name = os.path.basename(path)

    # Add filename to every page
    for page in pages:
        page.metadata["file_name"] = file_name

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(pages)

    return chunks

if __name__ == "__main__":
    pdf_path = "C:/Users/ASHUTOSH/Downloads/Ashutosh_Kumar_Resume_UPL_NextGenIntern.pdf"

    chunks = load_chunk(pdf_path)

    print("Total chunks:", len(chunks))

    print("\n--- First chunk metadata ---")
    print(chunks[0].metadata)