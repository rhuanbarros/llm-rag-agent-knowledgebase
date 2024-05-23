from pydantic import BaseModel
from typing import Dict, Optional, Tuple

class QueryParamsModel(BaseModel):
    Index_name: str
    Query: str
    Type: str
    Generate_answer: bool


class DocModel(BaseModel):
    # Metadata: Optional[Dict[str, str]] = None
    Content: str
    Source: str
    Page: str
    Filetype: str

class MessageModel(BaseModel):
    Type: str
    Content: str

class SearchResultModel(BaseModel):
    Results: list[DocModel]
    Generated_answer: str