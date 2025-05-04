import logging
from typing import Optional
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from config import Config

logger = logging.getLogger(__name__)

_llm = None
_llm_chain = None

def get_llm() -> ChatOpenAI:
    """
    Mendapatkan instance dari model Large Language Model (LLM).
    
    Returns:
        ChatOpenAI: Instance dari model LLM
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
    Mendapatkan chain LLM yang dikonfigurasi dengan prompt template yang sesuai.
    
    Returns:
        LLMChain: Chain LLM yang telah dikonfigurasi
    """
    global _llm_chain
    
    if _llm_chain is None:
        logger.info("Initializing LLM Chain...")
        
        # Membuat prompt template untuk RAG
        prompt_template = """
        Anda adalah asisten AI yang membantu menjawab pertanyaan berdasarkan informasi yang tersedia.
        
        Riwayat Percakapan:
        {chat_history}
        
        Konteks yang tersedia:
        {context}
        
        Pertanyaan Pengguna: {question}
        
        Berikan jawaban yang akurat berdasarkan konteks yang diberikan. Jika informasi tidak tersedia dalam konteks, 
        katakan bahwa Anda tidak memiliki informasi yang cukup untuk menjawab pertanyaan tersebut. 
        Jawaban harus:
        1. Informatif dan komprehensif
        2. Menggunakan konteks yang diberikan
        3. Dalam bahasa Indonesia yang baik dan benar
        4. Menggunakan format yang mudah dibaca
        
        Jawaban:
        """
        
        # Membuat prompt template dengan variabel yang diperlukan
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question", "chat_history"]
        )
        
        # Mendapatkan LLM
        llm = get_llm()
        
        # Membuat LLM Chain
        _llm_chain = LLMChain(
            llm=llm,
            prompt=PROMPT,
            verbose=True
        )
        
        logger.info("LLM Chain initialized")
    
    return _llm_chain