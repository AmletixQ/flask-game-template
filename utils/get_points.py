import requests

from flask import render_template, session
from constants import API_SECRET_KEY, API_URL


def get_points() -> int | None:
    headers = {
        "X-API-Key": API_SECRET_KEY
    }

    user_id = session.get("user_id")

    print(user_id)

    if not user_id:
        raise Exception("Не записан user_id в сессию.")

    response = requests.get(f"{API_URL}/users/{user_id}/points", headers=headers)

    if response.status_code != 200:
        raise Exception(f"Ошибка API: {response.text}")

    data = response.json()
    print(data)

    if isinstance(data, int):
        return data
    elif isinstance(data, dict):
        return data.get("points")
    
    return None
