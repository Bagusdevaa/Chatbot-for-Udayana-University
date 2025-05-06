import os
import logging
from typing import Optional, List
# Import dari langchain_community, bukan langchain
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from langchain.vectorstores.base import VectorStore

from config import Config
from app.RAG.document_loader import get_documents
from app.RAG.embeddings import get_embeddings
from app.utils import ensure_directory_exists

logger = logging.getLogger(__name__)

_vector_store = None
_retriever = None

def get_vector_store(force_rebuild=False) -> VectorStore:
    """
    Mendapatkan atau membuat vector store yang digunakan untuk menyimpan
    dan mengambil embeddings dokumen.
    
    Args:
        force_rebuild (bool): Jika True, paksa rebuild vector store meskipun sudah ada
    
    Returns:
        VectorStore: Instance vector store
    """
    global _vector_store
    
    if _vector_store is not None and not force_rebuild:
        return _vector_store
    
    logger.info("Initializing vector store...")
    
    # Pastikan direktori untuk vector store ada
    vector_store_path = Config.VECTOR_STORE_PATH
    ensure_directory_exists(vector_store_path)
    
    # Dapatkan embedding model
    embeddings = get_embeddings()
    
    try:
        # Jika force_rebuild = True atau vector store belum ada, buat yang baru
        if force_rebuild or not os.path.exists(vector_store_path) or not os.listdir(vector_store_path):
            logger.info("Creating new vector store from documents...")
            # Dapatkan dokumen
            documents = get_documents()
            
            if not documents or len(documents) == 0:
                logger.warning("No documents found to create vector store. Check your dataset.txt file.")
                raise ValueError("No documents found to create vector store")
            
            # Buat vector store baru
            _vector_store = Chroma.from_documents(
                documents=documents,
                embedding=embeddings,
                persist_directory=vector_store_path,
            )
            
            # Simpan vector store ke disk
            _vector_store.persist()
            logger.info(f"Vector store created and saved to {vector_store_path} with {len(documents)} documents")
        else:
            logger.info("Loading existing vector store...")
            _vector_store = Chroma(
                persist_directory=vector_store_path,
                embedding_function=embeddings,
            )
            logger.info(f"Vector store loaded from {vector_store_path}")
    
    except ImportError as e:
        logger.error(f"Error importing Chroma: {e}")
        # Menggunakan pesan yang lebih spesifik
        raise ImportError("Could not import ChromaDB. Please run: pip install -U chromadb langchain-community")
    except Exception as e:
        logger.error(f"Error creating vector store: {e}")
        raise
    
    return _vector_store

def get_retriever(force_rebuild_vector_store=False):
    """
    Mendapatkan retriever yang digunakan untuk mengambil dokumen yang relevan
    dengan query user.
    
    Args:
        force_rebuild_vector_store (bool): Jika True, paksa rebuild vector store
    
    Returns:
        Retriever: Instance retriever
    """
    global _retriever
    
    if _retriever is None or force_rebuild_vector_store:
        logger.info("Initializing retriever...")
        
        # Dapatkan vector store
        vector_store = get_vector_store(force_rebuild=force_rebuild_vector_store)
        
        # Buat retriever - menggunakan metode as_retriever dari VectorStore
        _retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}  # Mengambil 5 dokumen teratas yang paling relevan
        )
        
        logger.info("Retriever initialized")
    
    return _retriever