import os
from typing import Optional, Union, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'default-secret-key'
    DEBUG: bool = os.environ.get('DEBUG', 'False').lower() in ('true', 't', '1')
    
    # OpenAI API configuration
    OPENAI_API_KEY: Optional[str] = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL: str = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # RAG configuration
    EMBEDDINGS_MODEL: str = os.environ.get('EMBEDDINGS_MODEL', 'text-embedding-ada-002')
    VECTOR_STORE_PATH: str = os.path.join('data', 'vector_store')
    CHUNK_SIZE: int = int(os.environ.get('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP: int = int(os.environ.get('CHUNK_OVERLAP', 200))

    # Dataset configuration
    DATASET_PATH: str = os.path.join('data', 'dataset.txt')
    
    # Temperature for LLM model
    TEMPERATURE: float = float(os.environ.get('TEMPERATURE', 0.7))