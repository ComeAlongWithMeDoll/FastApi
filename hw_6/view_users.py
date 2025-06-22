from sqlmodel import Session, select
from database import engine
from models import User

with Session(engine) as session:
    users = session.exec(select(User)).all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Role: {user.role}")
