from typing import List, TypedDict

from flask import session
import requests

from constants import API_SECRET_KEY, API_URL


class Game(TypedDict):
    """
    Объект игры, который возвращается в качестве ответа из API
    """

    gameTitle: str
    gameId: int
    gamePublicationDate: str


def get_all_games() -> List[Game]:
    """
    Функция, которая обращается к API рудзынг и возвращает все игры разработчика
    """

    headers = {"X-API-Key": API_SECRET_KEY}

    response = requests.get(f"{API_URL}/games/my", headers=headers)
    response.raise_for_status()

    data = response.json()
    print(data)

    if isinstance(data, list):
        return data

    return []


def get_points() -> int | None:
    """
    Функция, которая обращается к API рудзынг и возвращает количество баллов у игрока
    """

    headers = {"X-API-Key": API_SECRET_KEY}

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


def login(email: str, password: str) -> str:
    """
    Функция, с помощью которой пользователь входит в свой аккаунт и получает свой userId
    """

    headers = {"X-API-Key": API_SECRET_KEY}

    user_data = {"email": email, "password": password}

    response = requests.post(
        f"{API_URL}/account/login", json=user_data, headers=headers
    )
    response.raise_for_status()

    data = response.json()
    user_id = None

    if isinstance(data, dict):
        user_id = data.get("userId")

    if not user_id:
        raise Exception("Не удалось получить ID пользователя")

    session["user_id"] = user_id

    return user_id


def ping():
    """
    Функция, которая проверяет жив ли API рудзынг
    """

    headers = {"X-API-Key": API_SECRET_KEY}

    response = requests.get(f"{API_URL}/ping", headers=headers)
    response.raise_for_status()

    if response.status_code != 200:
        raise Exception("Сервер недоступен")

    return response.json()


def post_points(amount: int) -> int:
    """
    Функция, с помощью которой разработчик начисляет баллы пользователю и отправляет их в API рудзынг
    """

    user_id = session.get("user_id")

    if not user_id:
        raise Exception("Не записан user_id в сессию.")

    games = get_all_games()
    game_id = None

    for game in games:
        if game.get("gameTitle") == "Тестовая игра":
            game_id = game.get("gameId")
            break
    else:
        raise Exception("Нет игры с таким названием")

    headers = {"X-API-Key": API_SECRET_KEY}

    response = requests.post(
        f"{API_URL}/users/{user_id}/games/{game_id}/points",
        json={"amount": amount},
        headers=headers,
    )

    if response.status_code != 200:
        raise Exception(f"Ошибка API: {response.text}")

    data = response.json()

    return data.get("newTotalPoints")

