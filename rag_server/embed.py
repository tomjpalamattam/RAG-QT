# embed.py
from langchain_qdrant import Qdrant
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from load_files import load_documents
from dotenv import load_dotenv
import os

load_dotenv()
hf_api_key = os.getenv("HF_API_KEY")

def get_embeddings():
    model = "Qwen/Qwen3-Embedding-8B"
    embeddings = HuggingFaceEndpointEmbeddings(
        model=model,
        task="feature-extraction",
        huggingfacehub_api_token = hf_api_key,
    )
    return embeddings

def index_documents(dir_path):
    documents = load_documents(dir_path)
    embeddings = get_embeddings()
    qdrant = Qdrant.from_documents(
        documents,
        embeddings,
        path="langchain_local_qdrant_pdf",
        collection_name="my_documents",
    )
    return len(documents)

def restore_db():
    embeddings = get_embeddings()
    qdrant = Qdrant.from_existing_collection(
        embeddings,
        path="langchain_local_qdrant_pdf",
        collection_name="my_documents",
    )
    return qdrant
