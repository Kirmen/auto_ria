import bot_data

from telegram import Bot


def send_message(message: str):
    token = bot_data.TOKEN
    chat_id = bot_data.CHAT_ID
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)


def send_message_with_photos(message: str, photos: str):
    token = bot_data.TOKEN
    chat_id = bot_data.CHAT_ID
    bot = Bot(token=token)

    bot.send_message(chat_id=chat_id, text=message)

    # for photo in photos:
    #     with open(photo, 'rb') as f:
    #         bot.send_photo(chat_id=CHAT_ID, photo=f)
