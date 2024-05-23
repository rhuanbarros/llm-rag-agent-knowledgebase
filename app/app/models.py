from pydantic import BaseModel
from typing import Dict, Optional, Tuple

class QueryParamsModel(BaseModel):
    index_name: str
    query: str
    type: str

class DocModel(BaseModel):
    # Metadata: Optional[Dict[str, str]] = None
    Content: str
    Source: str
    Page: str
    Filetype: str

class MessageModel(BaseModel):
    Type: str
    Content: str