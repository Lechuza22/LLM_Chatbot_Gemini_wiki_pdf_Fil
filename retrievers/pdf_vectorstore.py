import yaml
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def build_pdf_vectorstore(config):
    load_dotenv()
    api_key = os.getenv(config["llm"]["api_key_env_var"])

    if not api_key:
        raise ValueError("La API Key de Google no está definida en el archivo .env")

    pdf_paths = config["pdfs"]["paths"]
    chunk_size = config["retriever"]["chunk_size"]
    chunk_overlap = config["retriever"]["chunk_overlap"]

    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    for path in pdf_paths:
        loader = PyPDFLoader(path)
        docs = loader.load()
        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vectordb = FAISS.from_documents(all_chunks, embeddings)

    return vectordb
