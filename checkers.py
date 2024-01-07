import sqlite3
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from tg_tools import send_message


def check_price_changes(headers: Dict, hrefs: List[str]):
    conn = sqlite3.connect('auto_info.db')
    cursor = conn.cursor()

    cursor.execute('SELECT url, price FROM cars')
    results = cursor.fetchall()

    for url, current_price in results:
        for u in hrefs:
            if u == url:
                req = requests.get(url=u, headers=headers)
                soup = BeautifulSoup(req.content, "lxml")
                new_price = soup.find('div', class_='price_value').find('strong').get_text(strip=True)

                if new_price != current_price:
                    # send_message(f"Ціна на автомобіль {url} змінилася на {new_price}!")

                    cursor.execute('UPDATE cars SET price = ? WHERE url = ?', (new_price, url))
                    conn.commit()
    conn.close()


def check_sold_cars(hrefs: List):
    conn = sqlite3.connect('auto_info.db')
    cursor = conn.cursor()

    cursor.execute('SELECT url FROM cars')
    db_urls = [record[0] for record in cursor.fetchall()]

    for db_url in db_urls:
        if db_url not in hrefs:
            # send_message(f"Автомобіль {db_url} був проданий!")

            cursor.execute('DELETE FROM cars WHERE url = ?', (db_url,))
            conn.commit()

    conn.close()
