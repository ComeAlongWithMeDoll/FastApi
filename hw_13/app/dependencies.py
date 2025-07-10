from fastapi import Depends
from app.models import User

def get_current_user():
    # заглушка: возвращаем фиктивного пользователя
    return User(id=1, username="testuser")