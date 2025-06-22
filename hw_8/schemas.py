from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    text: str

class NoteUpdate(BaseModel):
    text: Optional[str] = None

class NoteOut(BaseModel):
    id: int
    text: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

class Token(BaseModel):
    access_token: str
    token_type: str