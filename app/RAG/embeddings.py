import os
import logging
from typing import Optional
from langchain.embeddings.openai import OpenAIEmbeddings
from config import Config

logger = logging.getLogger(__name__)

_embeddings: Optional[OpenAIEmbeddings] = None

def get_embeddings() -> OpenAIEmbeddings:
    """
    Get the embeddings model used to convert text into vectors.
    This function uses a singleton pattern to ensure there is only one instance
    of the embeddings model.
    
    Returns:
        OpenAIEmbeddings: Instance of the embeddings model
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