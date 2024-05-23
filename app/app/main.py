import uvicorn

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from operator import itemgetter

from typing import List
from typing import Dict, Optional, Tuple
from pydantic import BaseModel


# system
import os
import logging
import sys


from app.ingest import ingestService



os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = f"Procurador API"

logging.basicConfig(level=logging.INFO,  # Define o nível de log
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Define o formato da mensagem de log
                    stream=sys.stdout)  # Define a saída do log para stdout
# filename='app.log',  # Define o arquivo onde os logs serão gravados
# filemode='a')  # Define o modo de escrita do arquivo de log (append)






logging.info('Inicializando FastAPI')
app = FastAPI(title="Procurador API Server", description="API description")

logging.info('Configurando CORS')
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ingest_data_folder/", tags=["Data management"])
async def ingest_data_folder(folder_path: str, index_name: str):
    return ingestService.ingest_path(folder_path, index_name, logging)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
