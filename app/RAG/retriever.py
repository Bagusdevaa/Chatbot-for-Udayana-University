import os
import logging
from typing import Optional, List, Any
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from langchain.vectorstores.base import VectorStore
from langchain.schema.retriever import BaseRetriever

from config import Config
from app.RAG.document_loader import get_documents
from app.RAG.embeddings import get_embeddings
from app.utils import ensure_directory_exists

logger = logging.getLogger(__name__)

_vector_store: Optional[VectorStore] = None
_retriever: Optional[BaseRetriever] = None

def get_vector_store(force_rebuild: bool = False) -> VectorStore:
    """
    Get or create a vector store used to store and retrieve document embeddings.
    
    Args:
        force_rebuild (bool): If True, force rebuild the vector store even if it exists
    
    Returns:
        VectorStore: Vector store instance
    """
    global _vector_store
    
    if _vector_store is not None and not force_rebuild:
        return _vector_store
    
    logger.info("Initializing vector store...")
    
    # Ensure the directory for the vector store exists
    vector_store_path = Config.VECTOR_STORE_PATH
    ensure_directory_exists(vector_store_path)
    
    # Get the embedding model
    embeddings = get_embeddings()
    
    try:
        # If force_rebuild = True or vector store doesn't exist, create a new one
        if force_rebuild or not os.path.exists(vector_store_path) or not os.listdir(vector_store_path):
            logger.info("Creating new vector store from documents...")
            # Get the documents
            documents = get_documents()
            
            if not documents or len(documents) == 0:
                logger.warning("No documents found to create vector store. Check your dataset.txt file.")
                raise ValueError("No documents found to create vector store")
            
            # Create a new vector store
            _vector_store = Chroma.from_documents(
                documents=documents,
                embedding=embeddings,
                persist_directory=vector_store_path,
            )
            
            # Save the vector store to disk
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
        # Using a more specific message
        raise ImportError("Could not import ChromaDB. Please run: pip install -U chromadb langchain-community")
    except Exception as e:
        logger.error(f"Error creating vector store: {e}")
        raise
    
    return _vector_store

def get_retriever(force_rebuild_vector_store: bool = False) -> BaseRetriever:
    """
    Get a retriever used to retrieve documents relevant to the user's query.
    
    Args:
        force_rebuild_vector_store (bool): If True, force rebuild the vector store
    
    Returns:
        BaseRetriever: Retriever instance
    """
    global _retriever
    
    if _retriever is None or force_rebuild_vector_store:
        logger.info("Initializing retriever...")
        
        # Get the vector store
        vector_store = get_vector_store(force_rebuild=force_rebuild_vector_store)
        
        # Create a retriever - using the as_retriever method from VectorStore
        _retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}  # Get the top 5 most relevant documents
        )
        
        logger.info("Retriever initialized")
    
    return _retriever