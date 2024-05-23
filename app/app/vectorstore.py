from abc import ABC, abstractmethod

from app.embeddings import EmbeddingsService

from injector import inject

class VectorStoreService(ABC):
    @abstractmethod
    def index_docs(self, documents, embeddings, index_name: str):
        pass

# TODO: pass this when binding
WEAVIATE_URL = 'host.docker.internal'

class WeaviteVectorProvider(VectorStoreService):
    @inject
    def __init__(self, embeddingsService: EmbeddingsService):
        self.embeddingsService = embeddingsService
        self.embeddingsProvider = self.embeddingsService.get_provider()

    def get_weaviate_basic_client(self):
        import weaviate
        weaviate_client = weaviate.connect_to_custom(
            http_host=WEAVIATE_URL,
            http_port=8080,
            http_secure=False,
            grpc_host=WEAVIATE_URL,
            grpc_port=50051,
            grpc_secure=False,
            # auth_credentials=AuthApiKey(weaviate_key),   # `weaviate_key`: your Weaviate API key
        )

        return weaviate_client
    
    def index_docs(self, documents, index_name: str):
        weaviate_client = self.get_weaviate_basic_client()
        from langchain_weaviate.vectorstores import WeaviateVectorStore
        vector_store = WeaviateVectorStore.from_documents(documents,  self.embeddingsProvider, client=weaviate_client, index_name=index_name)
