from fastapi import HTTPException, status
from app.embeddings import embeddingsService
from app.vectorstore_weavite import weaviateService

VECTORE_STORE = 'weaviate'



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

        
        embeddings = embeddingsService.get_embedings()

        if VECTORE_STORE == 'weaviate':
            ingestService.index_docs_weavite(documents, embeddings, index_name)
        else:
            raise NotImplemented

        return "Ingestion succesfull"


ingestService = Ingest()

#