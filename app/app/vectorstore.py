import logging
from abc import ABC, abstractmethod

from app.models import QueryParamsModel
from app.embeddings import EmbeddingsService

from injector import inject

class VectorStoreService(ABC):
    @abstractmethod
    def index_docs(self, documents, embeddings, index_name: str):
        pass
    
    @abstractmethod
    def search_semantic_mmr(self, query_params: QueryParamsModel):
        pass

    @abstractmethod
    def search_semantic(self, query_params: QueryParamsModel):
        pass

    @abstractmethod
    def search_keyword(self, query_params: QueryParamsModel):
        pass
    
    @abstractmethod
    def search_hybrid(self, query_params: QueryParamsModel):
        pass

# TODO: pass this when binding
WEAVIATE_URL = 'host.docker.internal'

class WeaviteVectorProvider(VectorStoreService):
    @inject
    def __init__(self, embeddingsService: EmbeddingsService):
        logging.info('WeaviteVectorProvider instantiated')
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

    def get_vectorstore(self, index_name):
        from langchain_weaviate.vectorstores import WeaviateVectorStore
        weaviate_client = self.get_weaviate_basic_client()
        return WeaviateVectorStore(weaviate_client, index_name, "text", embedding=self.embeddingsProvider)
    
    def search_semantic_mmr(self, query_params: QueryParamsModel):
        vector_store = self.get_vectorstore(query_params.Index_name)
        retriever = vector_store.as_retriever(search_type="mmr")
        return retriever.invoke(query_params.Query)
    
    def get_retriever(self, index_name):
        vector_store = self.get_vectorstore(index_name)
        return vector_store.as_retriever(search_type="mmr")
        

    def search_semantic(self, query_params: QueryParamsModel):
        vector_store = self.get_vectorstore(query_params.Index_name)
        return vector_store.similarity_search(query_params.Query, alpha=1)

    def search_keyword(self, query_params: QueryParamsModel):
        vector_store = self.get_vectorstore(query_params.Index_name)
        return vector_store.similarity_search(query_params.Query, alpha=0)
    
    def search_hybrid(self, query_params: QueryParamsModel):
        vector_store = self.get_vectorstore(query_params.Index_name)
        return vector_store.similarity_search(query_params.Query, alpha=0.5)
        

