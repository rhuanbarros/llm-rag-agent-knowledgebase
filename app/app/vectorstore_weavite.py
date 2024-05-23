WEAVIATE_URL = 'host.docker.internal'

class WeaviteVectorStore():
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
    
    def index_docs_weavite(self, documents, embeddings, index_name: str):
        weaviate_client = self.get_weaviate_basic_client()
        from langchain_weaviate.vectorstores import WeaviateVectorStore
        vector_store = WeaviateVectorStore.from_documents(documents, embeddings, client=weaviate_client, index_name=index_name)

weaviateService = WeaviteVectorStore()