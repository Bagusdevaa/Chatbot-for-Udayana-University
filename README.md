# Udayana University Chatbot with RAG and LangChain

## Project Description
This project is an implementation of an informational chatbot for Udayana University using RAG (Retrieval Augmented Generation) technology and LangChain. The chatbot can answer user questions based on the provided Udayana University information dataset.

## Technologies Used
- **Flask**: Python web framework for the backend
- **LangChain**: Framework for creating AI applications with Large Language Models (LLM)
- **OpenAI API**: For LLM models and embeddings
- **Chroma DB**: Vector database for storing document embeddings
- **RAG (Retrieval Augmented Generation)**: Method to enhance LLM output with information from the dataset

## How RAG (Retrieval Augmented Generation) Works
1. **Dataset Processing**: 
   - The Udayana University information dataset is split into smaller chunks
   - Each chunk is converted into vector embeddings using OpenAI's embedding model
   - Embeddings are stored in a vector database (Chroma DB)

2. **Question-Answering Process**:
   - User submits a question through the web interface
   - The user's question is converted into embeddings
   - The system finds documents most relevant to the user's question using similarity search
   - Relevant documents are used as context for the LLM model
   - The LLM model (OpenAI GPT) generates an answer based on the provided context
   - The answer is sent back to the user

## Features
- **Knowledge Base Updates**: Admin can update the knowledge base directly from the UI
- **Context-Based Responses**: Answers are generated based on actual Udayana University data
- **Responsive Design**: Works on both desktop and mobile devices
- **Real-time Processing**: Instant responses with loading indicators

## Setup and Installation

### Prerequisites
- Python 3.8+ installed
- OpenAI account and API key
- Pip (Python package manager)

### Installation Steps
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatbot-udayana
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # For Windows
   venv\Scripts\activate
   # For macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the .env file**
   - Copy the `.env.example` file to `.env`
   - Add your OpenAI API key to the `.env` file
   ```bash
   cp .env.example .env
   # Edit the .env file and add your OPENAI_API_KEY
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the application**
   - Open your browser and visit `http://localhost:5000`

## Important Notes
- Ensure your OpenAI API key is securely stored and not shared
- Using the OpenAI API incurs costs, monitor your usage
- The dataset.txt file is used as the active dataset, while data/raw/dataset.txt serves as a backup
- The dataset.txt was last updated in 2023

## Updating the Knowledge Base
If you add new information to the dataset:
1. Update the `data/dataset.txt` file with new information
2. Use the "Update Knowledge" button in the UI to rebuild the vector database
3. The chatbot will now be able to answer questions based on the updated information

## License
This project is licensed under the [MIT License](LICENSE).
