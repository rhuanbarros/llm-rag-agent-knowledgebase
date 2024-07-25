# 🌟 LLM RAG Agent Knowledgebase 🌟

Welcome to the **LLM RAG Agent Knowledgebase**! 

This is a full-stack artificial intelligence project with both backend and frontend components. 🚀

## 📚 Project Overview

It was created an AI agent that can chat about document files ingested. 

It's designed to handle file ingestion, manage vector stores, chat with users, and perform advanced search queries.

### 🛠️ Key technologies

- **🌐 LangGraph**: Agent orchestration
- **🚀 FastAPI**: Backend framework for handling API operations.
- **📄 Unstructured Package**: For file ingestion and OCR.
- **🧠 Weaviate**: Vector store
- **🐳 Docker Compose**: For running Weaviate in a container.
- **🌐 C# Blazor**: Frontend framework for building the web application webassembly.


### 🛠️ Backend: API Project

The backend of this project is powered by **FastAPI**, enabling efficient handling of AI agent operations. Key features include:

- **File Ingestion**: 
  - **Unstructured Package**: Processes diverse types of files, including OCR for files in Portuguese.
  - **Chunk Splitting**: Files are split into smaller chunks to enhance semantic similarity during RAG (Retrieval-Augmented Generation) queries.
  
- **Vector Store**: 
  - **Weaviate**: Utilized as the vector store, running separately via a Docker Compose file.
  
- **Agent Capabilities**:
  - **Chat**: Engages in conversations and uses tools for specific tasks.
  - **Tool Use**: Currently supports vector store retrieval.
  - **Memory**: Saves conversation history using an SQLite database.

- **Search**:
  - **Endpoints**: Implements standard search in documents with keyword, semantic, and hybrid search capabilities.

### 🌐 Frontend: Web Project

The frontend is built using **C# Blazor**, providing a seamless and interactive user experience.

- **WebAssembly Project**: 
  - Runs entirely in the browser.
  - Fetches data from the backend API project.

## 🚀 Getting Started

To get started with the LLM RAG Agent Knowledgebase, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rhuanbarros/llm-rag-agent-knowledgebase.git
   ```

2. **Vector store Setup:**
    - Run the Weaviate server
   ```bash
   cd weaviate
   docker compose up
   ```

3. **Backend Setup:**
    - Open the `api`directory in the devcontainer using Vscode
    - Install Unstructured dependecies
   ```bash
    sudo apt update
    sudo apt install libmagic-dev -y
    sudo apt install poppler-utils -y
    sudo apt install tesseract-ocr -y
    sudo apt install tesseract-ocr-por -y  #portuguese language support
    sudo apt install libreoffice -y
   ```

    - Install dev dependencies
   ```bash
    sudo apt-get install graphviz graphviz-dev
   ```

    - Navigate to the `api` directory and install python dependencies.
   ```bash
    cd app
    poetry install
   ```
    
4. **Configure the OpenAI api key:**
    - Create a .env in the directory ./api/app with the following content:
    ```
    OPENAI_API_KEY=""
    ```

4. **Run the backend:**
   ```bash
    cd app
    source .venv/bin/activate
    fastapi dev procurador/main.py
   ```

4. **Ingest documents:**
    - Run the endpoint to ingest some example pdf files
    - go to url http://127.0.0.1:8000/docs#/Data%20management/ingest_data_folder_ingest_data_folder__post
    - run it


5. **Run the frontend:**
    - Open the `web`directory in the devcontainer using Vscode
   ```bash
    dotnet run
   ```
    
5. **Enjoy:**
    - Acces the webpage and chat with the llm