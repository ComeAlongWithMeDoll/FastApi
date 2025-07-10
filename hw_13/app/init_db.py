from app.database import Base, engine
from app import models  # Импортируйте все модели!

def create_db_and_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()