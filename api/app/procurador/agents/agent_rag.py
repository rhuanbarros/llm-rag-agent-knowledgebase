import logging
from injector import inject
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.documents.base import Document

from typing import List

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

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain.tools.retriever import create_retriever_tool

class AgentRagState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class AgentRag():
    @inject
    def __init__(self, llmService: LlmService, vectorStoreService: VectorStoreService, checkpointer, index_name: str):
        # initialize basic fields
        self.llmService = llmService
        self.vectorStoreService = vectorStoreService
        self.index_name = index_name

        self.llm = self.llmService.get_provider()
        self.retriever = self.vectorStoreService.get_retriever(self.index_name)

        self.prompt_system = """
            You are a smart research assistant. Use the vectorstore to look up information if needed. \
            You are allowed to make multiple calls (either together or in sequence). \
            Only look up information when you are sure of what you want. \
            If you need to look up some information before asking a follow up question, you are allowed to do that!
        """

        # create graph
        graph = StateGraph(AgentRagState)
        graph.add_node("llm", self.call_model)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges("llm", self.exists_action, {True: "action", False: END})
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
       
        # create tools
        tool = create_retriever_tool(
            self.retriever,
            "vectorstore",
            "Searches and returns excerpts from pdf files indexed",
        )
        tools = [tool]
        self.tools = {t.name: t for t in tools}
        # bind tools to the model
        self.model = self.llm.bind_tools(tools)

        # sets checkpointer memory
        self.graph = graph.compile(checkpointer=checkpointer)

    def call_model(self, state: AgentRagState):
        messages = state['messages']
        if self.prompt_system:
            messages = [SystemMessage(content=self.prompt_system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def exists_action(self, state: AgentRagState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def take_action(self, state: AgentRagState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}