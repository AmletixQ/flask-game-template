from typing import TypedDict, List

import requests
from constants import API_URL, API_SECRET_KEY

class Game(TypedDict):
    gameTitle: str
    gameId: int
    gamePublicationDate: str


def get_all_games() -> List[Game]:
    headers = {
        "X-API-Key": API_SECRET_KEY
    }


    response = requests.get(f"{API_URL}/games/my", headers=headers)
    response.raise_for_status()


    data = response.json()
    print(data)

    if isinstance(data, list):
        return data

    return []