import os
import logging
from typing import List, Optional
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config import Config
from app.utils import ensure_directory_exists

logger = logging.getLogger(__name__)

_documents: Optional[List[Document]] = None

def load_documents(force_reload: bool = False) -> List[Document]:
    """
    Load documents from dataset.txt and split them into smaller chunks.
    
    Args:
        force_reload (bool): If True, force reload documents even if already loaded
        
    Returns:
        List[Document]: List of processed documents
    """
    global _documents
    
    if _documents is not None and not force_reload:
        return _documents
    
    logger.info("Loading documents from dataset...")
    
    dataset_path = Config.DATASET_PATH
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset file not found at {dataset_path}")
    
    # Load the dataset file
    try:
        loader = TextLoader(dataset_path, encoding="utf-8")
        documents = loader.load()
        
        if not documents:
            logger.warning(f"No content loaded from {dataset_path}")
            return []
        
        logger.info(f"Successfully loaded raw documents from {dataset_path}")
        
        # Split the documents into chunks with better parameters
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n\n", "\n\n", "\n", " ", ""]
        )
        
        _documents = text_splitter.split_documents(documents)
        
        # Log some information about the processed documents
        logger.info(f"Loaded and split into {len(_documents)} document chunks")
        if _documents:
            avg_chunk_size = sum(len(doc.page_content) for doc in _documents) / len(_documents)
            logger.info(f"Average chunk size: {avg_chunk_size:.2f} characters")
            logger.info(f"Sample chunk content: {_documents[0].page_content[:100]}...")
        
        return _documents
    
    except Exception as e:
        logger.error(f"Error loading documents: {str(e)}")
        raise

def get_documents(force_reload: bool = False) -> List[Document]:
    """
    Get documents that have been loaded and processed.
    
    Args:
        force_reload (bool): If True, force reload documents
        
    Returns:
        List[Document]: List of processed documents
    """
    return load_documents(force_reload=force_reload)