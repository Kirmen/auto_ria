import os
from typing import List
import configparser

import requests

from photo_handlers import download_and_convert_photos

TELEGRAM_API_URL = "https://api.telegram.org/bot"

config = configparser.ConfigParser()
config.read('bot_data.config')

TOKEN = config.get('DEFAULT', 'TOKEN')
CHAT_ID = config.get('DEFAULT', 'CHAT_ID')


def send_message(message: str):
    token = TOKEN
    chat_id = CHAT_ID
    url = f"{TELEGRAM_API_URL}{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    response = requests.get(url, params=params)
    return response.json()


def send_message_with_photos(message: str, photos: List[str]):
    token = TOKEN
    chat_id = CHAT_ID
    url = f"{TELEGRAM_API_URL}{token}/sendPhoto"

    send_message(message)

    converted_photos = download_and_convert_photos(photos)
    for photo in converted_photos:
        with open(photo, 'rb') as f:
            files = {"photo": f}
            params = {"chat_id": chat_id}
            response = requests.post(url, params=params, files=files)

            if response.status_code != 200:
                print(f"Failed to send photo {photo}: {response.json()}")
        os.remove(photo)
