from app.models import DocModel, QueryParamsModel
from app.vectorstore import VectorStoreService

from injector import inject

class SearchService():
    @inject
    def __init__(self, vectorStoreService: VectorStoreService):
        self.vectorStoreService = vectorStoreService

    def conver_doc_to_DocModel_batch(self, results: list):
        searchResultsList = []
        for result in results:
            # TODO: put metadata
            doc = DocModel(Content=result.page_content)
            searchResultsList.append(doc)
        return searchResultsList

    def search_semantic(self, query_params: QueryParamsModel ):
        results = self.vectorStoreService.search_semantic(query_params)
        return self.conver_doc_to_DocModel_batch(results)
    
