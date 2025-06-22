from fastapi import FastAPI
from database import init_db
from users import router as users_router
from notes import router as notes_router

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(notes_router, prefix="/notes", tags=["notes"])

@app.on_event("startup")
def on_startup():
    init_db()
