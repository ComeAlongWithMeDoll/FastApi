from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import User
from security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register")
def register(username: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=username, password=get_password_hash(password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"msg": "User created"}

@router.post("/login")
def login(username: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}
