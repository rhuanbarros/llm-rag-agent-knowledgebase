import logging
from injector import inject
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.documents.base import Document

from typing import List

from procurador.config import ConfigService
from procurador.models import MessageModel
from procurador.services.vectorstore import VectorStoreService
from procurador.services.llm import LlmService

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from typing_extensions import TypedDict
from typing import List
from langchain_core.documents import Document

from langgraph.graph import END, StateGraph

class AgentRag():
    @inject
    def __init__(self, configService: ConfigService, llmService: LlmService, vectorStoreService: VectorStoreService):
        self.configService = configService
        self.llmService = llmService
        self.vectorStoreService = vectorStoreService

        self.llm_main = self.configService.options['llms']['main']

    def main_chain(self, query ):
        logging.info("main_chain")
        
        logging.info("query")
        logging.info(query)
        
        print("main_chain")
        
        print("query")
        print(query)