# This module contains RAG components for the chatbot
# Serves as an interface to access RAG components from outside the module

# Imports that cause problems have been moved into functions to avoid circular imports
# Imports will be done when the function is called, not when the module is loaded

from typing import List, Any
from langchain.schema import Document
from langchain.embeddings.base import Embeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.vectorstores.base import VectorStore
from langchain.schema.retriever import BaseRetriever

def get_documents(force_reload: bool = False) -> List[Document]:
    from app.RAG.document_loader import get_documents as _get_documents
    return _get_documents(force_reload=force_reload)

def load_documents(force_reload: bool = False) -> List[Document]:
    from app.RAG.document_loader import load_documents as _load_documents
    return _load_documents(force_reload=force_reload)

def get_embeddings() -> Embeddings:
    from app.RAG.embeddings import get_embeddings as _get_embeddings
    return _get_embeddings()

def get_llm() -> ChatOpenAI:
    from app.RAG.llm import get_llm as _get_llm
    return _get_llm()

def get_llm_chain() -> LLMChain:
    from app.RAG.llm import get_llm_chain as _get_llm_chain
    return _get_llm_chain()

def get_retriever(force_rebuild_vector_store: bool = False) -> BaseRetriever:
    from app.RAG.retriever import get_retriever as _get_retriever
    return _get_retriever(force_rebuild_vector_store=force_rebuild_vector_store)

def get_vector_store(force_rebuild: bool = False) -> VectorStore:
    from app.RAG.retriever import get_vector_store as _get_vector_store
    return _get_vector_store(force_rebuild=force_rebuild)

__all__ = [
    'get_documents',
    'load_documents',
    'get_embeddings',
    'get_llm',
    'get_llm_chain',
    'get_retriever',
    'get_vector_store'
]