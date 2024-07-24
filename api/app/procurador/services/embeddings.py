import logging
from abc import ABC, abstractmethod

class EmbeddingsService(ABC):
    @abstractmethod
    def get_provider(self):
        pass

class GPT4AllEmbeddingsProvider(EmbeddingsService):
    
    def get_provider(self):
        logging.info('GPT4AllEmbeddingsProvider - get_provider')
        
        from langchain_community.embeddings import GPT4AllEmbeddings
        
        model_name = "nomic-embed-text-v1.f16.gguf"

        gpt4all_kwargs = {'allow_download': 'True'}

        return GPT4AllEmbeddings(
            model_name=model_name,
            gpt4all_kwargs=gpt4all_kwargs
        )
