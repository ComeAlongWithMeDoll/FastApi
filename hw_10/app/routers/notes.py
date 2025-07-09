from fastapi import APIRouter

router = APIRouter()

@router.get("/notes")
def read_notes():
    return ["Note 1", "Note 2"]