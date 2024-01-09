import re
import sqlite3
from typing import Dict, List
# import time

import requests
from bs4 import BeautifulSoup

from checkers import check_price_changes, check_sold_cars
from db_tools import connect_to_db, put_in_db
from tg_tools import send_message_with_photos


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


def main(hrefs: List, headers: Dict):
    conn = sqlite3.connect('auto_info.db')
    cursor = conn.cursor()

    a = 0

    for url in hrefs:

        cursor.execute('SELECT url FROM cars WHERE url = ?', (url,))
        if cursor.fetchone():
            continue

        req = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(req.content, "lxml")

        photo_gal = soup.find('div', class_='preview-gallery').find_all('source')
        all_photo = []
        for photo in photo_gal:
            photo_small = photo.get('srcset')
            photo_full = re.sub(r'(\d+)s', r'\1f', photo_small)
            all_photo.append(photo_full)

        brand = 'Toyota'

        price = soup.find('div', class_='price_value').find('strong').get_text(strip=True)

        auction_url = 'no info'
        try:
            auction_url = soup.find('div', class_='vin-checked mb-15 _grey').find('a').get('href', auction_url)
        except AttributeError:
            pass

        auto_ria_url = url

        match = re.search(r'(\d+).html', url)
        car_id = match.group(1)
        print(car_id)

        message = f"Марка: {brand}\nЦіна: {price}\nПосилання: {auto_ria_url}\nПосилання на аукціон: {auction_url}"
        send_message_with_photos(message, all_photo)
        put_in_db(auto_ria_url, all_photo, brand, price, auction_url, car_id)

        a += 1
        if a == 3:
            break


def run():
    connect_to_db()

    while True:
        headers1 = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/109.0.5414.120 Safari/537.36 Avast/109.0.19987.120'

        }
        urls = get_all_hrefs(headers1)

        main(urls, headers1)
        check_sold_cars(urls)
        check_price_changes(headers1, urls)
        break

        # time.sleep(600)


if __name__ == '__main__':
    run()
