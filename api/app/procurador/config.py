import logging
from procurador.models import DocModel, QueryParamsModel
from procurador.services.vectorstore import VectorStoreService

from injector import inject

class ConfigService():
    @inject
    def __init__(self, options: dict):
        logging.info('ConfigService instantiated')
        logging.info(f'Options: {options}')

        self.options = options