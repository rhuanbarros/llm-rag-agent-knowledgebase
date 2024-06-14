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


from app.AgentReflectiveRetrieval import Agent, AgentReflectiveRetrieval
from app.agentBasic import AgentBasic
from app.llm import LlmService, OllamaLlmProvider
from app.search import SearchService
from app.models import *
from app.ingest import IngestService
from app.embeddings import EmbeddingsService, GPT4AllEmbeddingsProvider
from app.vectorstore import VectorStoreService, WeaviteVectorProvider


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = f"Procurador API"

logging.basicConfig(level=logging.INFO,  # Define o nível de log
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Define o formato da mensagem de log
                    stream=sys.stdout)  # Define a saída do log para stdout
# filename='app.log',  # Define o arquivo onde os logs serão gravados
# filemode='a')  # Define o modo de escrita do arquivo de log (append)






logging.info('Inicializando FastAPI')
app = FastAPI(title="Procurador API Server", description="API description")

logging.info('Configurando CORS')
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
async def ingest_data_folder(folder_path: str, index_name: str, ingestService: IngestService = Injected(IngestService) ):
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
        agent: AgentBasic = Injected(Agent)
    ):
    model = 'mistral'
    
    return agent.simple_message_chain(model, message)
    # return agent.main_chain([MessageModel(Type='Human', Content=message)], model)

@app.post("/reflective_retrieval/", tags=["Frontend"])
async def reflective_retrieval(
        message: str,
        agent: AgentReflectiveRetrieval = Injected(Agent)
    ):
    model = 'llama3'
    
    return agent.main_chain([MessageModel(Type='Human', Content=message)], model)


# inj = Injector()
inj = Injector(auto_bind=True)
inj.binder.bind(EmbeddingsService, to=GPT4AllEmbeddingsProvider)
inj.binder.bind(VectorStoreService, to=WeaviteVectorProvider)
inj.binder.bind(LlmService, to=OllamaLlmProvider)

attach_injector(app, inj)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
