from database import get_session
from models import User
from security import get_password_hash
from sqlmodel import Session, select
from database import engine

def hash_existing_passwords():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        for user in users:
        if not user.password.startswith("$2b@"):
            user.password = get_password_hash(user.password)
        session.commit()

if __name__ == "__main__":
    hash_existing_passwords()   