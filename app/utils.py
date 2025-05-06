import os
import logging
from typing import List, Dict, Any, Tuple, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_chat_history(chat_history: List[Dict[str, str]]) -> str:
    """
    Convert chat history from a list of dictionaries to a string format
    that can be used by the LLM.
    
    Args:
        chat_history: List of dictionaries in the format [{"role": "user", "content": "..."}, ...]
    
    Returns:
        String representation of the chat history in "Human: ... AI: ..." format
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
    Add a new question and answer to the chat history.
    
    Args:
        chat_history: Previous chat history
        question: User's question
        answer: System's answer
    
    Returns:
        Updated chat history
    """
    new_history = chat_history.copy() if chat_history else []
    
    # Add the user's question
    new_history.append({
        "role": "user",
        "content": question
    })
    
    # Add the system's answer
    new_history.append({
        "role": "assistant",
        "content": answer
    })
    
    # Limit the amount of history saved (optional)
    # This is to avoid tokens being too long
    max_history_items = 10  # Store 5 pairs of questions and answers
    if len(new_history) > max_history_items:
        new_history = new_history[-max_history_items:]
    
    return new_history

def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure the specified directory exists, if not, create the directory.
    
    Args:
        directory_path: Path to the directory to check/create
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logger.info(f"Created directory: {directory_path}")