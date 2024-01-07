import sqlite3
from typing import List


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


def put_in_db(auto_ria_url: str, all_photo: List, brand: str, price: str, auction_url: str, car_id: str):
    conn = sqlite3.connect('auto_info.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cars (url, photos, brand, price, auction_link, car_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (auto_ria_url, ','.join(all_photo), brand, price, auction_url, car_id))

    conn.commit()

    conn.close()
