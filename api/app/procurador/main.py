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
from procurador.agents.agent_basic import AgentBasic
from procurador.services.llm import LlmService, OllamaLlmProvider, OpenAILlmProvider
from procurador.services.search import SearchService
from procurador.models import *
from procurador.services.ingest import IngestService
from procurador.services.embeddings import EmbeddingsService, GPT4AllEmbeddingsProvider
from procurador.services.vectorstore import VectorStoreService, WeaviteVectorProvider

from langchain_core.messages import HumanMessage

import asyncio
import aiosqlite
from langgraph.checkpoint.aiosqlite import AsyncSqliteSaver
from langgraph.checkpoint.sqlite import SqliteSaver

from dotenv import load_dotenv

load_dotenv()


logging.basicConfig(level=logging.INFO,  # Define o nível de log
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Define o formato da mensagem de log
                    stream=sys.stdout)  # Define a saída do log para stdout

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

logging.info('Initializing Dependecy Injector')
inj = Injector(auto_bind=True)
inj.binder.bind(EmbeddingsService, to=GPT4AllEmbeddingsProvider)
inj.binder.bind(VectorStoreService, to=WeaviteVectorProvider)
# inj.binder.bind(LlmService, to=OllamaLlmProvider)
inj.binder.bind(LlmService, to=OpenAILlmProvider)

attach_injector(app, inj)


logging.info('Initializing Endpoints')

default_files_index_name = "index_files"

@app.post("/ingest_data_folder/", tags=["Data management"])
async def ingest_data_folder(folder_path: str = "../docs", index_name: str = default_files_index_name, ingestService: IngestService = Injected(IngestService) ):
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

@app.post("/simple_message/", tags=["Frontend"])
async def simple_message(
        message: str,
        model_name: str = None,
        agent: AgentBasic = Injected(AgentBasic)
    ):    
    return agent.simple_message_chain(message, model_name)

@app.post("/chat/", tags=["Frontend"], response_model=MessageModel)
async def chat(
        message: MessageModel,
    ):
    thread = {"configurable": {"thread_id": "2"}}

    messages = [HumanMessage(content=message.Content)]
    # messages = [HumanMessage(content=message)]

    llmService = inj.get(LlmService)
    vectorStoreService = inj.get(VectorStoreService)

    async with AsyncSqliteSaver.from_conn_string("checkpoints_memory.db") as checkpointer:    
        agent = AgentRag(llmService=llmService, vectorStoreService=vectorStoreService, checkpointer=checkpointer, index_name=default_files_index_name)

        response = await agent.graph.ainvoke({"messages": messages}, thread)

        answer = response['messages'][-1].content
        return MessageModel(Type='AI', Content=answer)
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
