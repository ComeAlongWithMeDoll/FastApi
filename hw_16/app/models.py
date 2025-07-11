from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

Base = SQLModel

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_completed: bool = Field(default=False)



