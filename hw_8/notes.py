from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import get_session
from models import Note
from schemas import NoteCreate, NoteUpdate, NoteOut
from security import get_current_user
from models import User

router = APIRouter()

@router.post("/notes", response_model=NoteOut)
def create_note(note: NoteCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    new_note = Note(text=note.text, owner_id=user.id)
    session.add(new_note)
    session.commit()
    session.refresh(new_note)
    return new_note

@router.get("/notes", response_model=list[NoteOut])
def read_notes(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    search: str = Query(None)
):
    query = select(Note).where(Note.owner_id == user.id)
    if search:
        query = query.where(Note.text.contains(search))
    notes = session.exec(query.offset(skip).limit(limit)).all()
    return notes

@router.get("/notes/{note_id}", response_model=NoteOut)
def read_note(note_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    note = session.get(Note, note_id)
    if not note or note.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/notes/{note_id}", response_model=NoteOut)
def update_note(note_id: int, update: NoteUpdate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    note = session.get(Note, note_id)
    if not note or note.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    if update.text:
        note.text = update.text
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@router.delete("/notes/{note_id}")
def delete_note(note_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    note = session.get(Note, note_id)
    if not note or note.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return {"msg": "Note deleted"}
