from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas import NoteRead, NoteCreate
from app.models import User
from app.database import get_db
from app.redis_cache import redis_cache
from app import crud
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/notes", response_model=List[NoteRead])
async def get_notes(user: User = Depends(get_current_user), skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    key = f"notes:{user.id}:{skip}:{limit}"
    cached = await redis_cache.get(key)
    if cached:
        return cached

    notes = crud.get_notes(db, user.id, skip, limit)
    result = [NoteRead.from_orm(note).dict() for note in notes]
    await redis_cache.set(key, result)
    return result

@router.post("/notes", response_model=NoteRead)
async def create_note(note: NoteCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_note = crud.create_note(db, note, user.id)
    await redis_cache.delete_pattern(f"notes:{user.id}*")
    return new_note

@router.put("/notes/{note_id}", response_model=NoteRead)
async def update_note(note_id: int, note: NoteCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_note = crud.update_note(db, note_id, note, user.id)
    await redis_cache.delete_pattern(f"notes:{user.id}*")
    return updated_note

@router.delete("/notes/{note_id}")
async def delete_note(note_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_note(db, note_id, user.id)
    await redis_cache.delete_pattern(f"notes:{user.id}*")
    return {"message": "Deleted"}
