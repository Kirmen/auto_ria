from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from db_tools import DatabaseManager
from tg_tools import send_message


def check_price_changes(headers: Dict, hrefs: List[str]):
    with DatabaseManager() as db:
        cursor = db

        cursor.execute('SELECT url, price FROM cars')
        results = cursor.fetchall()

        for db_url, current_price in results:
            for fresh_url in hrefs:
                if fresh_url == db_url:
                    req = requests.get(url=fresh_url, headers=headers)
                    soup = BeautifulSoup(req.content, "lxml")
                    new_price = soup.find('div', class_='price_value').find('strong').get_text(strip=True)

                    if new_price != current_price:
                        send_message(f"Ціна на автомобіль {db_url} змінилася на {new_price}!")

                        cursor.execute('UPDATE cars SET price = ? WHERE url = ?', (new_price, db_url))


def check_sold_cars(hrefs: List):
    with DatabaseManager() as db:
        cursor = db

        cursor.execute('SELECT url FROM cars')
        db_urls = [record[0] for record in cursor.fetchall()]

        for db_url in db_urls:
            if db_url not in hrefs:
                send_message(f"Автомобіль {db_url} був проданий!")

                cursor.execute('DELETE FROM cars WHERE url = ?', (db_url,))
