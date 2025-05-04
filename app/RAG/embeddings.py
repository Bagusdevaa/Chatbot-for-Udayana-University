import os
import logging
from typing import Optional
from langchain.embeddings.openai import OpenAIEmbeddings
from config import Config

logger = logging.getLogger(__name__)

_embeddings = None

def get_embeddings() -> OpenAIEmbeddings:
    """
    Mendapatkan model embeddings yang digunakan untuk mengubah teks menjadi vektor.
    Fungsi ini menggunakan singleton pattern untuk memastikan hanya ada satu instance
    dari model embeddings.
    
    Returns:
        OpenAIEmbeddings: Instance model embeddings
    """
    global _embeddings
    
    if _embeddings is None:
        logger.info("Initializing embeddings model...")
        api_key = Config.OPENAI_API_KEY
        
        if not api_key:
            raise ValueError("OpenAI API key is required for embeddings. Please set OPENAI_API_KEY in .env file.")
        
        _embeddings = OpenAIEmbeddings(
            model=Config.EMBEDDINGS_MODEL,
            openai_api_key=api_key
        )
        logger.info(f"Embeddings model initialized: {Config.EMBEDDINGS_MODEL}")
    
    return _embeddings