import requests

BASE_URL = "http://127.0.0.1:8000"

def get_token(username, password):
    response = requests.post(f"{BASE_URL}/login", json={
        "username": username,
        "password": password,
        "role": "user"  
    })

    if response.status_code != 200:
        print("Ошибка входа:", response.text)
        return None

    token = response.json().get("access_token")
    return token

def get_admin_users(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{BASE_URL}/admin/users", headers=headers)

    if response.status_code == 200:
        print("Доступ разрешён. Список пользователей:")
        print(response.json())
    else:
        print("Ошибка доступа:", response.status_code, response.text)

if __name__ == "__main__":
    username = "adminuser"
    password = "adminpass"

    token = get_token(username, password)
    if token:
        get_admin_users(token)
