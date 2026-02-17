import requests

from flask import render_template, session
from constants import API_URL


def get_points() -> int:
    user_id = session.get("user_id")
    print(user_id)

    if not user_id:
        raise Exception("Не записан user_id в сессию.")

    response = requests.get(f"{API_URL}/users/{user_id}/points")

    if response.status_code != 200:
        raise Exception(f"Ошибка API: {response.text}")

    data = response.json()

    if isinstance(data, dict):
        return data.get("points");

    return None
