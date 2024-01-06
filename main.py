import re
import sqlite3
from typing import Dict, List
# import time

import requests
from bs4 import BeautifulSoup
from telegram import Bot

import bot_data


def connect_to_db():
    conn = sqlite3.connect('auto_info.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY,
        url TEXT,
        photos TEXT,
        brand TEXT,
        price TEXT,
        auction_link TEXT,
        car_id TEXT
    )
    ''')


def put_in_db(auto_ria_url, all_photo, brand, price, auction_url, car_id):
    conn = sqlite3.connect('auto_info.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cars (url, photos, brand, price, auction_link, car_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (auto_ria_url, ','.join(all_photo), brand, price, auction_url, car_id))

    conn.commit()

    conn.close()


def send_message(message):
    token = bot_data.TOKEN
    chat_id = bot_data.CHAT_ID
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)


def send_message_with_photos(message, photos):
    token = bot_data.TOKEN
    chat_id = bot_data.CHAT_ID
    bot = Bot(token=token)

    bot.send_message(chat_id=chat_id, text=message)

    # for photo in photos:
    #     with open(photo, 'rb') as f:
    #         bot.send_photo(chat_id=CHAT_ID, photo=f)


def check_price_changes(headers):
    conn = sqlite3.connect('auto_info.db')
    cursor = conn.cursor()

    cursor.execute('SELECT url, price FROM cars')
    results = cursor.fetchall()

    for url, current_price in results:
        req = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(req.content, "lxml")
        new_price = soup.find('div', class_='price_value').find('strong').get_text(strip=True)

        if new_price != current_price:
            # send_message(f"Ціна на автомобіль {url} змінилася на {new_price}!")

            cursor.execute('UPDATE cars SET price = ? WHERE url = ?', (new_price, url))
            conn.commit()
    conn.close()


def check_sold_cars(hrefs):
    conn = sqlite3.connect('auto_info.db')
    cursor = conn.cursor()

    for u in hrefs:
        cursor.execute('SELECT url FROM cars WHERE url = ?', (u,))
        if not cursor.fetchone():
            # send_message(f"Автомобіль {u} був проданий!")
            pass

    conn.close()


def get_all_hrefs(headers: Dict) -> List:
    all_hrefs = []
    for i in range(20):
        url = f'https://auto.ria.com/uk/search/?indexName=auto&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.usa.not=-1&country.import.id=840&price.currency=1&abroad.not=0&custom.not=1&page={i}&size=10'
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        hrefs = soup.find_all('a', class_='m-link-ticket')
        if len(hrefs) == 0:
            break
        for h in hrefs:
            all_hrefs.append(h.get('href'))
    return all_hrefs


def get_info_and_put_in_db(hrefs, headers):
    conn = sqlite3.connect('auto_info.db')
    cursor = conn.cursor()
    a = 0
    for u in hrefs:
        print(a)
        print(u)
        cursor.execute('SELECT url FROM cars WHERE url = ?', (u,))
        if cursor.fetchone():
            continue

        req = requests.get(url=u, headers=headers)
        soup = BeautifulSoup(req.content, "lxml")

        photo_gal = soup.find('div', class_='preview-gallery').find_all('source')
        all_photo = []
        for p in photo_gal:
            photo_s = p.get('srcset')
            photo_f = re.sub(r'(\d+)s', r'\1f', photo_s)
            all_photo.append(photo_f)

        brand = 'Toyota'

        price = soup.find('div', class_='price_value').find('strong').get_text(strip=True)

        auction_url = 'no info'
        try:
            auction_url = soup.find('div', class_='vin-checked mb-15 _grey').find('a').get('href', auction_url)
        except AttributeError:
            pass

        auto_ria_url = u

        match = re.search(r'(\d+).html', u)
        car_id = match.group(1)
        print(car_id)

        # message = f"Марка: {brand}\nЦіна: {price}\nПосилання: {auto_ria_url}\nПосилання на аукціон: {auction_url}"
        # send_message_with_photos(message, all_photo)
        put_in_db(auto_ria_url, all_photo, brand, price, auction_url, car_id)

        a += 1
        if a == 3:
            break


def main():
    connect_to_db()

    while True:
        headers1 = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/109.0.5414.120 Safari/537.36 Avast/109.0.19987.120'

        }
        urls = get_all_hrefs(headers1)

        get_info_and_put_in_db(urls, headers1)
        check_price_changes(headers1)
        check_sold_cars(urls)
        break

        # time.sleep(600)


main()
