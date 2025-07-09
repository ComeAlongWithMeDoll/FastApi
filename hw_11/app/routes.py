from fastapi import APIRouter, Depends
from app.tasks import send_mock_email

router = APIRouter()

@router.post("/trigger-task")
def trigger_task():
    send_mock_email.delay("user@example.com")
    return {"message": "Task started"}
