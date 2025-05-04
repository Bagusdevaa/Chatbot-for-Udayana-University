import os
import logging
from typing import List, Dict, Any, Tuple

# Setup logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_chat_history(chat_history: List[Dict[str, str]]) -> str:
    """
    Mengubah format riwayat chat dari list of dictionaries menjadi string format
    yang dapat digunakan oleh LLM.
    
    Args:
        chat_history: List of dictionaries dengan format [{"role": "user", "content": "..."}, ...]
    
    Returns:
        String representasi dari chat history dalam format "Human: ... AI: ..."
    """
    if not chat_history:
        return ""
    
    formatted_history = []
    for entry in chat_history:
        role = entry.get("role", "")
        content = entry.get("content", "")
        
        if role.lower() == "user":
            formatted_history.append(f"Human: {content}")
        elif role.lower() == "assistant":
            formatted_history.append(f"AI: {content}")
    
    return "\n".join(formatted_history)

def save_chat_history(chat_history: List[Dict[str, str]], 
                     question: str, 
                     answer: str) -> List[Dict[str, str]]:
    """
    Menambahkan pertanyaan dan jawaban baru ke dalam riwayat chat.
    
    Args:
        chat_history: Riwayat chat sebelumnya
        question: Pertanyaan pengguna
        answer: Jawaban dari sistem
    
    Returns:
        Riwayat chat yang telah diperbarui
    """
    new_history = chat_history.copy() if chat_history else []
    
    # Tambahkan pertanyaan pengguna
    new_history.append({
        "role": "user",
        "content": question
    })
    
    # Tambahkan jawaban sistem
    new_history.append({
        "role": "assistant",
        "content": answer
    })
    
    # Batasi jumlah riwayat yang disimpan (opsional)
    # Ini untuk menghindari token yang terlalu panjang
    max_history_items = 10  # Menyimpan 5 pasang pertanyaan dan jawaban
    if len(new_history) > max_history_items:
        new_history = new_history[-max_history_items:]
    
    return new_history

def ensure_directory_exists(directory_path: str) -> None:
    """
    Memastikan direktori yang ditentukan ada, jika tidak, buat direktori.
    
    Args:
        directory_path: Path ke direktori yang akan diperiksa/dibuat
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Created directory: {directory_path}")