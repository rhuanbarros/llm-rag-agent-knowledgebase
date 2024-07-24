import uvicorn

from fastapi import FastAPI, HTTPException

from injector import Injector
from fastapi_injector import attach_injector, Injected

from fastapi.middleware.cors import CORSMiddleware

from operator import itemgetter

from typing import List
from typing import Dict, Optional, Tuple
from pydantic import BaseModel


# system
import os
import logging
import sys


from procurador.agents.agent_rag import AgentRag
from procurador.config import ConfigService
from procurador.agents.agent_reflective_retrieval import AgentReflectiveRetrieval
from procurador.agents.agent_basic import AgentBasic
from procurador.services.llm import LlmService, OllamaLlmProvider
from procurador.services.search import SearchService
from procurador.models import *
from procurador.services.ingest import IngestService
from procurador.services.embeddings import EmbeddingsService, GPT4AllEmbeddingsProvider
from procurador.services.vectorstore import VectorStoreService, WeaviteVectorProvider


logging.basicConfig(level=logging.INFO,  # Define o nível de log
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Define o formato da mensagem de log
                    stream=sys.stdout)  # Define a saída do log para stdout
# filename='app.log',  # Define o arquivo onde os logs serão gravados
# filemode='a')  # Define o modo de escrita do arquivo de log (append)



logging.info('Initializing FastAPI')
app = FastAPI(title="LLM RAG Knowledgebase API Server", description="API endpoints")

logging.info('CORS settings')
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ingest_data_folder/", tags=["Data management"])
async def ingest_data_folder(folder_path: str = "../docs", index_name: str = "index_files", ingestService: IngestService = Injected(IngestService) ):
    return ingestService.ingest_path(folder_path, index_name)

@app.post("/search/", response_model=list[DocModel], tags=["Frontend"])
async def search(
        query_params: QueryParamsModel, 
        searchService: SearchService = Injected(SearchService), 
    ):

    if query_params.Type == 'semantic':
        return searchService.search_semantic(query_params)
    elif query_params.Type == 'keyword':
        return searchService.search_keyword(query_params)
    elif query_params.Type == 'hybrid':
        return searchService.search_hybrid(query_params)
    else:
        raise HTTPException(status_code=400, detail="QueryParamsModel.Type should be a valid type.")        



@app.post("/chat/", response_model=MessageModel, tags=["Frontend"])
async def chat(
        chatHistory: List[MessageModel],
        # agent: Agent = Injected(Agent)
    ):
    pass


@app.post("/simple_message/", tags=["Frontend"])
async def simple_message(
        message: str,
        agent: AgentBasic = Injected(AgentBasic)
    ):
    model = 'mistral'
    
    return agent.simple_message_chain(model, message)
    # return agent.main_chain([MessageModel(Type='Human', Content=message)], model)

@app.post("/agent_rag/", tags=["Frontend"])
async def agent_rag(
        message = 'como acessar o pje?',
        agent: AgentRag = Injected(AgentRag)
    ):

    return agent.main_chain('como acessar o pje?')

# @app.post("/reflective_retrieval/", tags=["Frontend"])
# async def reflective_retrieval(
#         message: str,
#         agent: AgentReflectiveRetrieval = Injected(AgentReflectiveRetrieval)
#     ):
#     model = 'llama3'
    
#     return agent.main_chain([MessageModel(Type='Human', Content=message)], model)


configs = {
    'llms': {
        'main': 'llama3',
        'secondary': 'mistral',
        'tertiary': 'mistral'
    },
    'index_name': 'index_1',
    # 'embeddings': '',
    # 'vector_store': '',
}


# inj = Injector()
inj = Injector(auto_bind=True)
inj.binder.bind(EmbeddingsService, to=GPT4AllEmbeddingsProvider)
inj.binder.bind(VectorStoreService, to=WeaviteVectorProvider)
inj.binder.bind(LlmService, to=OllamaLlmProvider)
inj.binder.bind(ConfigService, to=ConfigService(configs))

attach_injector(app, inj)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
