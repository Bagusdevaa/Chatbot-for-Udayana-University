from flask import Blueprint, render_template, request, jsonify
from app.RAG.retriever import get_retriever
from app.RAG.llm import get_llm_chain
from app.utils import get_chat_history, save_chat_history

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
        
        # Mendapatkan dokumen yang relevan dengan pertanyaan pengguna
        context_docs = retriever.get_relevant_documents(question)
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        # Mengolah pertanyaan dengan konteks yang telah diambil
        response = llm_chain.run(question=question, 
                                context=context_text, 
                                chat_history=get_chat_history(chat_history))
        
        # Menyimpan riwayat chat untuk konteks future
        new_history = save_chat_history(chat_history, question, response)
        
        return jsonify({
            "answer": response,
            "history": new_history
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "error": "Terjadi kesalahan saat memproses permintaan Anda.",
            "details": str(e)
        }), 500