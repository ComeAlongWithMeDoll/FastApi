from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import User
from schemas import UserCreate, Token
from database import get_session
from security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password, role=user.role)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"msg": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(form_data: UserCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}