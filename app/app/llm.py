import logging
from abc import ABC, abstractmethod

class LlmService(ABC):
    @abstractmethod
    def get_provider(self):
        pass

class OllamaLlmProvider(LlmService):

    def get_provider(self, model_name, temperature=0.5,):
        logging.info('OllamaLlmProvider - get_provider')

        url = 'http://host.docker.internal:11434'
        
        from langchain_community.chat_models import ChatOllama

        return ChatOllama(model=model_name, temperature=temperature, base_url=url)