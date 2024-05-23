import logging
from app.models import DocModel, QueryParamsModel
from app.vectorstore import VectorStoreService

from injector import inject

class SearchService():
    @inject
    def __init__(self, vectorStoreService: VectorStoreService):
        logging.info('SearchService instantiated')
        self.vectorStoreService = vectorStoreService

    def conver_doc_to_DocModel_batch(self, results: list):
        searchResultsList = []
        for result in results:
            # TODO: put metadata
            doc = DocModel(Content=result.page_content)
            searchResultsList.append(doc)
        return searchResultsList

    def search_semantic(self, query_params: QueryParamsModel ):
        logging.info('SearchService search_semantic')
        results = self.vectorStoreService.search_semantic(query_params)
        return self.conver_doc_to_DocModel_batch(results)
    
    def search_keyword(self, query_params: QueryParamsModel ):
        logging.info('SearchService search_keyword')
        results = self.vectorStoreService.search_keyword(query_params)
        return self.conver_doc_to_DocModel_batch(results)
    
    def search_hybrid(self, query_params: QueryParamsModel ):
        logging.info('SearchService search_hybrid')
        results = self.vectorStoreService.search_hybrid(query_params)
        return self.conver_doc_to_DocModel_batch(results)
    
