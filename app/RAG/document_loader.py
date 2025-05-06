import os
import logging
from typing import List, Optional
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config import Config
from app.utils import ensure_directory_exists

logger = logging.getLogger(__name__)

_documents = None

def load_documents(force_reload=False) -> List[Document]:
    """
    Memuat dokumen dari dataset.txt dan membagi dokumen menjadi chunk yang lebih kecil.
    
    Args:
        force_reload (bool): Jika True, paksa reload dokumen meskipun sudah dimuat
        
    Returns:
        List[Document]: List dari dokumen yang telah diproses
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

def get_documents(force_reload=False) -> List[Document]:
    """
    Mendapatkan dokumen yang telah dimuat dan diproses.
    
    Args:
        force_reload (bool): Jika True, paksa reload dokumen
        
    Returns:
        List[Document]: List dari dokumen yang telah diproses
    """
    return load_documents(force_reload=force_reload)