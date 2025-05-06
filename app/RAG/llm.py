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
        
        # Membuat prompt template untuk RAG yang telah disempurnakan
        prompt_template = """
        Anda adalah asisten AI khusus untuk Universitas Udayana yang membantu menjawab pertanyaan 
        tentang universitas, program studi, pendaftaran, dan informasi lainnya berdasarkan data yang tersedia.
        
        Riwayat Percakapan:
        {chat_history}
        
        Berikut ini adalah konteks yang berisi informasi yang relevan dengan pertanyaan pengguna:
        {context}
        
        Pertanyaan Pengguna: {question}
        
        Berikan jawaban yang akurat dan informatif berdasarkan konteks yang diberikan. 
        Jawaban harus:
        1. Fokus pada informasi terkait Universitas Udayana
        2. Menggunakan informasi dari konteks yang diberikan 
        3. Informatif dan komprehensif
        4. Dalam bahasa Indonesia yang baik dan benar
        5. Menggunakan format yang mudah dibaca
        
        Jika informasi tidak tersedia dalam konteks, katakan dengan jujur bahwa Anda tidak memiliki 
        informasi yang cukup untuk menjawab pertanyaan tersebut, tetapi Anda akan dengan senang hati 
        membantu pengguna mendapatkan informasi dari sumber resmi Universitas Udayana.
        
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