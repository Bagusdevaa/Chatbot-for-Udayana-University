from flask import Blueprint, render_template, request, jsonify, Response
from typing import Dict, List, Any, Optional, Tuple, Union
from app.RAG.retriever import get_retriever
from app.RAG.llm import get_llm_chain
from app.utils import get_chat_history, save_chat_history
import logging

logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

@main.route('/')
def index() -> str:
    """Render the main chatbot page."""
    return render_template('index.html')

@main.route('/api/chat', methods=['POST'])
def chat() -> Tuple[Response, int]:
    """API endpoint to process user questions."""
    data = request.json
    question = data.get('question', '')
    chat_history = data.get('history', [])
    
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400
    
    try:
        # Get the initialized retriever
        retriever = get_retriever()
        
        # Get the configured LLM chain
        llm_chain = get_llm_chain()
        
        # Log the user's question
        logger.info(f"User question: {question}")
        
        # Get documents relevant to the user's question
        context_docs = retriever.get_relevant_documents(question)
        
        # Log the number of documents found
        logger.info(f"Retrieved {len(context_docs)} relevant documents")
        
        # Combine the content of relevant documents
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        # Log the context that will be used (truncated for log)
        logger.info(f"Context preview: {context_text[:200]}...")
        
        # Process the question with the retrieved context
        response = llm_chain.run(
            question=question, 
            context=context_text, 
            chat_history=get_chat_history(chat_history)
        )
        
        # Log the response for debugging
        logger.info(f"AI response: {response[:100]}...")
        
        # Save chat history for future context
        new_history = save_chat_history(chat_history, question, response)
        
        return jsonify({
            "answer": response,
            "history": new_history
        }), 200
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({
            "error": "An error occurred while processing your request.",
            "details": str(e)
        }), 500

@main.route('/api/rebuild-index', methods=['POST'])
def rebuild_index() -> Tuple[Response, int]:
    """Endpoint to force rebuild the vector store."""
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
        }), 200
    
    except Exception as e:
        logger.error(f"Error rebuilding index: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500