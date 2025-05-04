import os
import logging
from typing import Optional, List
from langchain.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from langchain.vectorstores.base import VectorStore
from langchain.retrievers import VectorStoreRetriever

from config import Config
from app.RAG.document_loader import get_documents
from app.RAG.embeddings import get_embeddings
from app.utils import ensure_directory_exists

logger = logging.getLogger(__name__)

_vector_store = None
_retriever = None

def get_vector_store() -> VectorStore:
    """
    Mendapatkan atau membuat vector store yang digunakan untuk menyimpan
    dan mengambil embeddings dokumen.
    
    Returns:
        VectorStore: Instance vector store
    """
    global _vector_store
    
    if _vector_store is not None:
        return _vector_store
    
    logger.info("Initializing vector store...")
    
    # Pastikan direktori untuk vector store ada
    vector_store_path = Config.VECTOR_STORE_PATH
    ensure_directory_exists(vector_store_path)
    
    # Dapatkan embedding model
    embeddings = get_embeddings()
    
    # Periksa apakah vector store sudah ada
    if os.path.exists(vector_store_path) and os.listdir(vector_store_path):
        logger.info("Loading existing vector store...")
        _vector_store = Chroma(
            persist_directory=vector_store_path,
            embedding_function=embeddings
        )
    else:
        logger.info("Creating new vector store from documents...")
        # Dapatkan dokumen
        documents = get_documents()
        
        # Buat vector store baru
        _vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=vector_store_path
        )
        
        # Simpan vector store ke disk
        _vector_store.persist()
        logger.info(f"Vector store created and saved to {vector_store_path}")
    
    return _vector_store

def get_retriever() -> VectorStoreRetriever:
    """
    Mendapatkan retriever yang digunakan untuk mengambil dokumen yang relevan
    dengan query user.
    
    Returns:
        VectorStoreRetriever: Instance retriever
    """
    global _retriever
    
    if _retriever is None:
        logger.info("Initializing retriever...")
        
        # Dapatkan vector store
        vector_store = get_vector_store()
        
        # Buat retriever
        _retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}  # Mengambil 3 dokumen teratas yang paling relevan
        )
        
        logger.info("Retriever initialized")
    
    return _retriever