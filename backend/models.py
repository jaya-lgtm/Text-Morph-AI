from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    display_name: Optional[str] = ""

class TextData(BaseModel):
    username: str
    text: str
    summary: str
    paraphrase: str
    source_name: Optional[str] = "Pasted Text"