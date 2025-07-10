from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int
    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True