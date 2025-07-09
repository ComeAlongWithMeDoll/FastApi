from time import sleep
from celery_app import celery_app

@celery_app.task
def send_mock_email(email: str):
    print(f"Sending email to {email}...")
    sleep(10)
    print(f"Email sent to {email}")
