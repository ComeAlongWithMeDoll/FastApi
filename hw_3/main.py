from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select, SQLModel
from database import get_session
from models import User
from schemas import UserCreate
from security import get_password_hash, verify_password
from database import engine

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/register")
def register(user: UserCreate):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.username == user.username)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, password=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}