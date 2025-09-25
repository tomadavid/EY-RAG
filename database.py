from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from api import api_key
from langchain_huggingface import HuggingFaceEmbeddings

with open("data.txt", "r", encoding="utf-8") as f:
    docs = f.read()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
chunks = splitter.split_text(docs)

model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_store = Chroma(
    collection_name="ey_data",
    embedding_function=model,
    persist_directory="./chroma_db"
)

vector_store.add_texts(
    texts=chunks,
    metadatas=[{"source": "cv.txt"} for _ in chunks],
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

print(f"Persisted to disk {vector_store._collection.count()} files")
