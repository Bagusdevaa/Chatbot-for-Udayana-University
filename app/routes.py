from flask import Blueprint, render_template, request, jsonify
from app.RAG.retriever import get_retriever
from app.RAG.llm import get_llm_chain
from app.utils import get_chat_history, save_chat_history
import logging

logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Render halaman utama chatbot."""
    return render_template('index.html')

@main.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint API untuk mengolah pertanyaan pengguna."""
    data = request.json
    question = data.get('question', '')
    chat_history = data.get('history', [])
    
    if not question:
        return jsonify({"error": "Pertanyaan tidak boleh kosong"}), 400
    
    try:
        # Mengambil retriever yang telah diinisialisasi
        retriever = get_retriever()
        
        # Mengambil chain LLM yang telah dikonfigurasi
        llm_chain = get_llm_chain()
        
        # Mencatat pertanyaan pengguna
        logger.info(f"User question: {question}")
        
        # Mendapatkan dokumen yang relevan dengan pertanyaan pengguna
        context_docs = retriever.get_relevant_documents(question)
        
        # Log jumlah dokumen yang ditemukan
        logger.info(f"Retrieved {len(context_docs)} relevant documents")
        
        # Gabungkan konten dokumen yang relevan
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        # Log konteks yang akan digunakan (truncated untuk log)
        logger.info(f"Context preview: {context_text[:200]}...")
        
        # Mengolah pertanyaan dengan konteks yang telah diambil
        response = llm_chain.run(
            question=question, 
            context=context_text, 
            chat_history=get_chat_history(chat_history)
        )
        
        # Log respon untuk debugging
        logger.info(f"AI response: {response[:100]}...")
        
        # Menyimpan riwayat chat untuk konteks future
        new_history = save_chat_history(chat_history, question, response)
        
        return jsonify({
            "answer": response,
            "history": new_history
        })
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Terjadi kesalahan saat memproses permintaan Anda.",
            "details": str(e)
        }), 500

@main.route('/api/rebuild-index', methods=['POST'])
def rebuild_index():
    """Endpoint untuk memaksa rebuild vector store."""
    try:
        from app.RAG.document_loader import get_documents
        from app.RAG.retriever import get_retriever
        
        # Force reload documents
        docs = get_documents(force_reload=True)
        
        # Force rebuild vector store
        retriever = get_retriever(force_rebuild_vector_store=True)
        
        return jsonify({
            "success": True,
            "message": f"Successfully rebuilt index with {len(docs)} documents"
        })
    
    except Exception as e:
        logger.error(f"Error rebuilding index: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500