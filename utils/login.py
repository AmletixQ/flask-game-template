from flask import session
import requests

from constants import API_SECRET_KEY, API_URL


def login(email: str, password: str) -> str:
    headers = {
        "X-API-Key": API_SECRET_KEY
    }

    user_data = {"email": email, "password": password}

    response = requests.post(f"{API_URL}/account/login", json=user_data, headers=headers)
    response.raise_for_status()

    data = response.json()
    user_id = None

    if isinstance(data, dict):
        user_id = data.get("userId")

    if not user_id:
        raise Exception("Не удалось получить ID пользователя")

    session["user_id"] = user_id

    return user_id
