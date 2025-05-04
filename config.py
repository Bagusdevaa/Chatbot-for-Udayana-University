import os
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci-rahasia-default'
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', 't', '1')
    
    # OpenAI API configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # RAG configuration
    EMBEDDINGS_MODEL = os.environ.get('EMBEDDINGS_MODEL', 'text-embedding-ada-002')
    VECTOR_STORE_PATH = os.path.join('data', 'vector_store')
    CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', 200))

    # Dataset configuration
    DATASET_PATH = os.path.join('data', 'dataset.txt')
    
    # Temperature untuk model LLM
    TEMPERATURE = float(os.environ.get('TEMPERATURE', 0.7))