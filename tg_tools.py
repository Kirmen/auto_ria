import os
from typing import List

from telegram import Bot

from photo_handlers import download_and_convert_photos
import bot_data


def send_message(message: str):
    token = bot_data.TOKEN
    chat_id = bot_data.CHAT_ID
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)


def send_message_with_photos(message: str, photos: List[str]):
    token = bot_data.TOKEN
    chat_id = bot_data.CHAT_ID
    bot = Bot(token=token)

    bot.send_message(chat_id=chat_id, text=message)

    converted_photos = download_and_convert_photos(photos)
    for photo in converted_photos:
        with open(photo, 'rb') as f:
            bot.send_photo(chat_id=chat_id, photo=f)

        os.remove(photo)
