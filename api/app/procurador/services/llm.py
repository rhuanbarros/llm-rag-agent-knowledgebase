import logging
from abc import ABC, abstractmethod

class LlmService(ABC):
    @abstractmethod
    def get_provider(self):
        pass

class OpenAILlmProvider(LlmService):

    def get_provider(self, model_name=None, temperature=0.5, json=False):
        logging.info('OpenAILlmProvider - get_provider')

        if not model_name:
            model_name = 'gpt-4o-mini'
        logging.info(f'Using model name: {model_name}')
       
        from langchain_openai import ChatOpenAI

        if json:
            # When using this option, the chat conversation needs to have a system message with the string 'json' in some place like 'Output in json'.
            return ChatOpenAI(model=model_name, temperature=0.5).bind(
                response_format={"type": "json_object"}
            )
        else:
            return ChatOpenAI(model=model_name, temperature=0.5)

# not in use anymore
class OllamaLlmProvider(LlmService):

    def get_provider(self, model_name, temperature=0.5, format=None):
        logging.info('OllamaLlmProvider - get_provider')

        url = 'http://host.docker.internal:11434'
        
        from langchain_community.chat_models import ChatOllama

        if format:
            return ChatOllama(model=model_name, temperature=temperature, base_url=url, format=format)
        else:
            return ChatOllama(model=model_name, temperature=temperature, base_url=url)