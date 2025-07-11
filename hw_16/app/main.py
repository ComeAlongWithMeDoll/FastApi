from fastapi import FastAPI, Depends
from app.database import async_session, init_db
from app.models import Note
from app.crud import create_note, get_notes
from sqlmodel.ext.asyncio.session import AsyncSession

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/notes/")
async def create(note: Note, session: AsyncSession = Depends(async_session)):
    return await create_note(session, note)

@app.get("/notes/")
async def read(session: AsyncSession = Depends(async_session)):
    return await get_notes(session)
