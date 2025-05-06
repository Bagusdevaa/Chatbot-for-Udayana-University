import logging
from typing import Optional
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from config import Config

logger = logging.getLogger(__name__)

_llm: Optional[ChatOpenAI] = None
_llm_chain: Optional[LLMChain] = None

def get_llm() -> ChatOpenAI:
    """
    Get an instance of the Large Language Model (LLM).
    
    Returns:
        ChatOpenAI: Instance of the LLM model
    """
    global _llm
    
    if _llm is None:
        logger.info("Initializing LLM...")
        api_key = Config.OPENAI_API_KEY
        
        if not api_key:
            raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY in .env file.")
        
        _llm = ChatOpenAI(
            model_name=Config.OPENAI_MODEL,
            temperature=Config.TEMPERATURE,
            openai_api_key=api_key,
            verbose=True
        )
        
        logger.info(f"LLM initialized: {Config.OPENAI_MODEL}")
    
    return _llm

def get_llm_chain() -> LLMChain:
    """
    Get an LLM chain configured with the appropriate prompt template.
    
    Returns:
        LLMChain: The configured LLM chain
    """
    global _llm_chain
    
    if _llm_chain is None:
        logger.info("Initializing LLM Chain...")
        
        # Create an enhanced prompt template for RAG
        prompt_template = """
        You are an AI assistant specifically for Udayana University that helps answer questions
        about the university, study programs, registration, and other information based on available data.
        
        Conversation History:
        {chat_history}
        
        The following is context containing information relevant to the user's question:
        {context}
        
        User Question: {question}
        
        Provide an accurate and informative answer based on the given context.
        The answer should:
        1. Focus on information related to Udayana University
        2. Use information from the provided context
        3. Be informative and comprehensive
        4. Be in good and correct Indonesian language
        5. Use a format that is easy to read
        
        If the information is not available in the context, honestly state that you do not have
        enough information to answer the question, but you would be happy to
        help the user get information from the official Udayana University sources.
        
        Answer:
        """
        
        # Create a prompt template with the required variables
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question", "chat_history"]
        )
        
        # Get the LLM
        llm = get_llm()
        
        # Create the LLM Chain
        _llm_chain = LLMChain(
            llm=llm,
            prompt=PROMPT,
            verbose=True
        )
        
        logger.info("LLM Chain initialized")
    
    return _llm_chain