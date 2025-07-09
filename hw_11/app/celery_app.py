from celery import Celery
import os

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=broker_url,
)

celery_app.conf.task_routes = {
    "app.tasks.send_mock_email": {"queue": "emails"},
}
