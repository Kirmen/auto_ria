import sqlite3
from typing import List


class DatabaseManager:
    def __init__(self, db_name='auto_info.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


def create_db():
    with DatabaseManager() as cursor:
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


def put_to_db(cursor: sqlite3.Cursor, auto_ria_url: str, all_photo: List, brand: str, price: str, auction_url: str, car_id: str):
    cursor.execute('''
        INSERT INTO cars (url, photos, brand, price, auction_link, car_id)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (auto_ria_url, ','.join(all_photo), brand, price, auction_url, car_id))


def is_url_in_db(url: str, cursor: sqlite3.Cursor) -> bool:
    cursor.execute('SELECT url FROM cars WHERE url = ?', (url,))
    return bool(cursor.fetchone())
