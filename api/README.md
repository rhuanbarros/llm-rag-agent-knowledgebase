# Procurador.API.server

# How to setup the server
    - Run the project in the devcontainer
    - install Unstructured dependecies
            sudo apt update
            sudo apt install libmagic-dev -y
            sudo apt install poppler-utils -y
            sudo apt install tesseract-ocr -y
            sudo apt install tesseract-ocr-por -y  #portuguese language support
            sudo apt install libreoffice -y
    - install dev dependencies
            sudo apt-get install graphviz graphviz-dev  
    - cd app
    - poetry install

    - open a terminal ouside the devcontainer
    - cd weaviate
    - docker compose up
    - run the endpoint to ingest some pdf files
    - go to url http://127.0.0.1:8000/docs#/Data%20management/ingest_data_folder_ingest_data_folder__post
    - run it
    - take a look at the log in the terminal
    - run the server
    - run the frontend
    - try search and ask llm


# how to run
    in the app directory
    source .venv/bin/activate
    fastapi dev procurador/main.py

    First call to the api it downloads the embeddings model, so it could be slow.

# Dependecy injector project used
    https://github.com/python-injector/injector
    
# Weaviate docs
    
    docker compose up

    This works
    https://pypi.org/project/langchain-weaviate/
    https://python.langchain.com/v0.1/docs/integrations/vectorstores/weaviate/
    https://github.com/langchain-ai/langchain-weaviate/tree/main/libs/weaviate
    https://github.com/langchain-ai/langchain-weaviate/blob/main/libs/weaviate/langchain_weaviate/vectorstores.py

    the following docs dont work ->   https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.weaviate.Weaviate.html 

# Ollama command to run local

docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama


# TODO
    - create a uid in the frontend at the start of the conversation and pass it to the backend
    - indexing files using ParentDocumentRetriever to use the longer context of gpt4o
        https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/parent_document_retriever/
    - email indexing
        - use to index the email with metadata and the cleaned version with report in multiple vectors
            https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/multi_vector/ 
    - index google drive documents
    
    
# Useful links
    - https://github.com/langchain-ai/langgraph/blob/main/examples/persistence_postgres.ipynb


