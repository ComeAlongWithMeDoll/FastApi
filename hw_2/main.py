from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from models import User
from schemas import UserCreate, UserLogin
from database import get_sesion, init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/register")
def register(user_create: UserCreate, session: Session = Depends(get_sesion)):
    statement = select(User).where(User.username == user_create.username)
    user = session.exec(statement).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(username=user_create.username, password=user_create.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"id":new_user.id, "username":new_user.username}

@app.post("/login")
def login(user_login: UserLogin, session: Session = Depends(get_sesion)):
    statement = select(User).where(User.username == user_login.username)
    user = session.exec(statement).first()
    if not user or user.password != user_login.password:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return{"message": "Login successful"}