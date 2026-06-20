# ingest.py

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def build_index():
    print("Loading documents...")

    loader = DirectoryLoader(
        "data",
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local("faiss_index")

    print("FAISS index saved successfully!")

if __name__ == "__main__":
    build_index()