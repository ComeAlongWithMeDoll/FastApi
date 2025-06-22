from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    role: str = "User"

    notes: List["Note"] = Relationship(back_populates="owner")

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="notes")