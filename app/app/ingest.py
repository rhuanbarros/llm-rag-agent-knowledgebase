from fastapi import HTTPException, status

WEAVIATE_URL = 'host.docker.internal'

class Ingest():
    def get_langchain_docs(self, elements, filename):
        from unstructured.chunking.title import chunk_by_title
        from langchain_core.documents import Document

        # create chunks to better rag
        chunks = chunk_by_title(elements, max_characters=1500, new_after_n_chars=1000, overlap=150)
        
        documents = []
        # convert to the Langchain format
        for chunk in chunks:
            metadata = chunk.metadata.to_dict()
            # print("---------------------")
            # print(metadata)
            # print("---------------------")
            # print(chunk.text)

            del metadata["languages"]
            if "filename" in metadata:
                metadata["source"] = metadata["filename"]
            else:
                metadata["source"] = filename

            documents.append(Document(page_content=chunk.text, metadata=metadata))

        return documents
    
    # TODO: create another class to abstract this
    def get_embedings(self):
        from langchain_community.embeddings import GPT4AllEmbeddings
        
        model_name = "nomic-embed-text-v1.f16.gguf"

        gpt4all_kwargs = {'allow_download': 'True'}

        return GPT4AllEmbeddings(
            model_name=model_name,
            gpt4all_kwargs=gpt4all_kwargs
        )
    
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

    def ingest_path(self, folder_path: str, index_name: str, logging):
        logging.info('Importing files to the vector store')

        from unstructured.partition.auto import partition        

        import os
        try:
            path, dirs, files = next(os.walk(folder_path))
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verify the path submited"
            )

        if not path:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verify the path submited"
            )
                
        documents_all = []
        for file in files:
            with open( os.path.join(path, file), 'rb') as f:
                logging.info(f'Opening file: {file}')
                
                # open file, clean, segment
                elements = partition(file=f)
                
                documents = self.get_langchain_docs(elements, file)
                documents_all.extend(documents)

        
        embeddings = self.get_embedings()

        weaviate_client = self.get_weaviate_basic_client()

        from langchain_weaviate.vectorstores import WeaviateVectorStore
        vector_store = WeaviateVectorStore.from_documents(documents, embeddings, client=weaviate_client, index_name=index_name)

        return "Ingestion succesfull"


ingest = Ingest()

#