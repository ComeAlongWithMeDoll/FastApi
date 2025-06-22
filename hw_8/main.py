from fastapi import FastAPI
from database import create_db_and_tables
from users import router as users_router
from notes import router as notes_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(users_router, prefix="/users")
app.include_router(notes_router)