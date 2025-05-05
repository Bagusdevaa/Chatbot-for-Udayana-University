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

def load_documents() -> List[Document]:
    """
    Memuat dokumen dari dataset.txt dan membagi dokumen menjadi chunk yang lebih kecil.
    
    Returns:
        List[Document]: List dari dokumen yang telah diproses
    """
    global _documents
    
    if _documents is not None:
        return _documents
    
    logger.info("Loading documents from dataset...")
    
    dataset_path = Config.DATASET_PATH
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset file not found at {dataset_path}")
    
    # Load the dataset file
    loader = TextLoader(dataset_path, encoding="utf-8")
    documents = loader.load()
    
    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        length_function=len,
        # Menghapus parameter is_separator_regex yang sudah tidak didukung
    )
    
    _documents = text_splitter.split_documents(documents)
    logger.info(f"Loaded and split {len(_documents)} document chunks from dataset")
    
    return _documents

def get_documents() -> List[Document]:
    """
    Mendapatkan dokumen yang telah dimuat dan diproses.
    
    Returns:
        List[Document]: List dari dokumen yang telah diproses
    """
    if _documents is None:
        return load_documents()
    return _documents