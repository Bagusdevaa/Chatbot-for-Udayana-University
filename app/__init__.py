from flask import Flask
from typing import Optional
from config import Config

def create_app(config_class=Config) -> Flask:
    """
    Create and configure the Flask application.
    
    Args:
        config_class: Configuration class for the application
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='../templates')
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Ensure API key is set
    if not app.config.get('OPENAI_API_KEY'):
        app.logger.warning("OpenAI API key is not set! Please add it to your .env file.")
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Initialize RAG components (if needed on startup)
    # This could be done lazily instead to save resources
    # from app.RAG.document_loader import initialize_document_loader
    # initialize_document_loader()
    
    return app