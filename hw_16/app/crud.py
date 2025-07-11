from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Note
from sqlmodel import select

async def create_note(session: AsyncSession, note: Note):
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note

async def get_notes(session: AsyncSession):
    result = await session.exec(select(Note))
    return result.all()