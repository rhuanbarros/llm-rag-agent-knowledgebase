from pydantic import BaseModel
from typing import Dict, Optional, Tuple

class QueryParamsModel(BaseModel):
    index_name: str
    query: str

class DocModel(BaseModel):
    Metadata: Optional[Dict[str, str]] = None
    Content: str

class MessageModel(BaseModel):
    Type: str
    Content: str