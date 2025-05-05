# Modul ini mengandung komponen-komponen RAG untuk chatbot
# Berfungsi sebagai interface untuk mengakses komponen RAG dari luar modul

# Impor yang menyebabkan masalah telah dipindahkan ke dalam fungsi untuk menghindari impor melingkar
# Impor akan dilakukan saat fungsi dipanggil, bukan saat modul dimuat

def get_documents():
    from app.RAG.document_loader import get_documents as _get_documents
    return _get_documents()

def load_documents():
    from app.RAG.document_loader import load_documents as _load_documents
    return _load_documents()

def get_embeddings():
    from app.RAG.embeddings import get_embeddings as _get_embeddings
    return _get_embeddings()

def get_llm():
    from app.RAG.llm import get_llm as _get_llm
    return _get_llm()

def get_llm_chain():
    from app.RAG.llm import get_llm_chain as _get_llm_chain
    return _get_llm_chain()

def get_retriever():
    from app.RAG.retriever import get_retriever as _get_retriever
    return _get_retriever()

def get_vector_store():
    from app.RAG.retriever import get_vector_store as _get_vector_store
    return _get_vector_store()

__all__ = [
    'get_documents',
    'load_documents',
    'get_embeddings',
    'get_llm',
    'get_llm_chain',
    'get_retriever',
    'get_vector_store'
]