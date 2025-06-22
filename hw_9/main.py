from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from task9.database import init_db, get_session
from task9.schemas import UserCreate, UserLogin, NoteCreate, NoteUpdate, NoteOut
from task9.crud import create_user, get_user_by_username, create_note, get_notes_by_user, get_note, delete_note
from task9.security import verify_password, create_access_token
from task9.dependencies import get_current_user
from task9.models import User, Note

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Pаботает"}

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/register")
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    existing_user = await get_user_by_username(session, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = await create_user(session, user.username, user.password)
    return {"id": new_user.id, "username": new_user.username}

@app.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    existing_user = await get_user_by_username(session, user.username)
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": existing_user.username})

    return {
        "message": "Login successful",
        "username": existing_user.username,
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username}

@app.post("/notes", response_model=NoteOut)
async def create_user_note(note: NoteCreate, session: AsyncSession = Depends(get_session), user = Depends(get_current_user)):
    return await create_note(session, note.text, user.id)

@app.get("/notes", response_model=List[NoteOut])
async def read_notes(session: AsyncSession = Depends(get_session), user = Depends(get_current_user)):
    return await get_notes_by_user(session, user.id)

@app.get("/notes/{note_id}", response_model=NoteOut)
async def read_note(note_id: int, session: AsyncSession = Depends(get_session), user = Depends(get_current_user)):
    note = await get_note(session, note_id, user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.delete("/notes/{note_id}")
async def delete_user_note(note_id: int, session: AsyncSession = Depends(get_session), user = Depends(get_current_user)):
    note = await get_note(session, note_id, user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await delete_note(session, note)
    return {"ok": True}