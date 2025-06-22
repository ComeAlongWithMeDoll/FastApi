from sqlalchemy.future import select
from task9.models import User, Note
from task9.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(session: AsyncSession, username: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_username(session: AsyncSession, username: str) -> User:
    statement = select(User).where(User.username == username)
    result = await session.execute(statement)
    return result.scalar_one_or_none()

async def create_note(session: AsyncSession, text: str, user_id: int) -> Note:
    note = Note(text=text, owner_id=user_id)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note

async def get_notes_by_user(session: AsyncSession, user_id: int) -> Note:
    result = await session.execute(select(Note).where(Note.owner_id == user_id))
    return result.scalars().all()

async def get_note(session: AsyncSession, note_id: int, user_id: int) -> Note:
    result = await session.execute(select(Note).where(Note.id == note_id, Note.owner_id == user_id))
    return result.scalar_one_or_none()

async def delete_note(session: AsyncSession, note) -> Note:
    await session.delete(note)
    await session.commit()