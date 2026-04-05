import requests

from flask import session
from constants import API_SECRET_KEY, API_URL
from utils.get_all_games import get_all_games



def post_points(amount: int) -> int:
    user_id = session.get("user_id")

    if not user_id: raise Exception("Не записан user_id в сессию.")

    games = get_all_games()
    game_id = None

    for game in games:
        if game.get("gameTitle") == "Тестовая игра":
            game_id = game.get("gameId")
            break
    else:
        raise Exception("Нет игры с таким названием")

    headers = {
        "X-API-Key": API_SECRET_KEY
    }

    response = requests.post(
        f"{API_URL}/users/{user_id}/games/{game_id}/points",
        json={"amount": amount},
        headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"Ошибка API: {response.text}")

    data = response.json()

    return data.get("newTotalPoints")
