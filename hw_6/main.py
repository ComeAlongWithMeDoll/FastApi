from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from database import engine, get_session, create_db_and_tables
from schemas import UserCreate, Token
from security import (
    create_access_token,
    verify_password,
    get_password_hash,
    get_current_user,
    require_role
)
from models import User

app = FastAPI()

# Инициализация БД при запуске
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password, role=user.role)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/login", response_model=Token)
def login(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    }


@app.get("/admin/users", dependencies=[Depends(require_role("admin"))])
def get_all_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users
