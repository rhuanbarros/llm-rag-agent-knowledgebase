import logging
from injector import inject
from procurador.services.vectorstore import VectorStoreService
from procurador.services.llm import LlmService


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
