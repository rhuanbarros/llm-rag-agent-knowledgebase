# Procurador.API.server

# TODO

    - I was creating the AgentRag using the notebook
    - I should get the old code from the other project to create the chat with history
    - better to remember the basic chains functionality usgin langchain in the notebbok 
    - also I should create this notebook as a cheatsheet to remember later



# how to run

cd app
source .venv/bin/activate
fastapi dev procurador/main.py

# Dependecy injector
    https://github.com/python-injector/injector
    

# Unstructured
    sudo apt update
    sudo apt install libmagic-dev -y
    sudo apt install poppler-utils -y
    sudo apt install tesseract-ocr -y
    sudo apt install tesseract-ocr-por -y  #portuguese language support
    sudo apt install libreoffice -y

# Weaviate docs
    
    docker compose up

    This works
    https://pypi.org/project/langchain-weaviate/
    https://python.langchain.com/v0.1/docs/integrations/vectorstores/weaviate/
    https://github.com/langchain-ai/langchain-weaviate/tree/main/libs/weaviate
    https://github.com/langchain-ai/langchain-weaviate/blob/main/libs/weaviate/langchain_weaviate/vectorstores.py



    the following docs dont work ->   https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.weaviate.Weaviate.html 

# Ollama

docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama