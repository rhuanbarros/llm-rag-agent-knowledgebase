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

from langgraph.graph import END, StateGraph

class AgentBasic():
    
    @inject
    def __init__(self, llmService: LlmService, vectorStoreService: VectorStoreService):
        self.llmService = llmService
        self.vectorStoreService = vectorStoreService

    def simple_message_chain(self, message, model=None):

        prompt_system = """
            You are a helpful assistant who is answer all the folling questions.
        """
        prompt_user = """
            {MESSAGE}
        """

        from langchain_core.prompts import ChatPromptTemplate

        prompt_conversation = ChatPromptTemplate.from_messages([
            ("system", prompt_system), 
            ("user", prompt_user)
            ])

        llm = self.llmService.get_provider(model)

        chain = prompt_conversation | llm

        return chain.invoke({'MESSAGE': message})

    # def summary_chain(self, docs: list[Document]):
    #     prompt = PromptTemplate(
    #         template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> 
    #         You are an assistant for helping summarizing documents. 
    #         Use the following pieces of retrieved documents to generate a summary. 
            
    #         Use four sentences maximum and keep the answer concise. no preamble or explanation<|eot_id|><|start_header_id|>user<|end_header_id|>

    #         Context: {context} 
    #         Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
    #         input_variables=["question", "document"],
    #     )

    #     llm = ChatOllama(model=self.model_name, temperature=0, base_url=self.url_ollama)


    #     # Post-processing
    #     def format_docs(docs):
    #         return "\n\n".join(doc.page_content for doc in docs)


    #     # Chain
    #     rag_chain = prompt | llm | StrOutputParser()

    #     return rag_chain.invoke({"context": docs})
