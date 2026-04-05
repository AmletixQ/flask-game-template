import requests
from constants import API_SECRET_KEY, API_URL


def ping():
    headers = {
        "X-API-Key": API_SECRET_KEY
    }

    response = requests.get(f"{API_URL}/ping", headers=headers)
    response.raise_for_status()

    if response.status_code != 200:
        raise Exception("Сервер недоступен")
    
    return response.json()