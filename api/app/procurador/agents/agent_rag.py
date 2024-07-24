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
    def __init__(self, llmService: LlmService, vectorStoreService: VectorStoreService):
        self.llmService = llmService
        self.vectorStoreService = vectorStoreService

        self.llm = self.llmService.get_provider(self.llm_main_name)
        self.retriever = self.vectorStoreService.get_retriever(self.index_name)

    def main_chain(self, query ):
        logging.info("main_chain")
        
