from pydantic import BaseModel
from typing import Dict, Optional, Tuple

class QueryParamsModel(BaseModel):
    Index_name: str
    Query: str
    Type: str
    
class DocModel(BaseModel):
    # Metadata: Optional[Dict[str, str]] = None
    Content: str
    Source: str
    Page: str
    Filetype: str

class MessageModel(BaseModel):
    Type: str
    Content: str
