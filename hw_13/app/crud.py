from sqlalchemy.orm import Session
from app import models, schemas

def get_notes(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Note).filter(models.Note.user_id == user_id).offset(skip).limit(limit).all()

def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note_id: int, note: schemas.NoteCreate, user_id: int):
    db_note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.user_id == user_id).first()
    if db_note:
        db_note.title = note.title
        db_note.content = note.content
        db.commit()
        db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int, user_id: int):
    db_note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.user_id == user_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note