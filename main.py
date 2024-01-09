import time

from checkers import check_price_changes, check_sold_cars
from db_tools import create_db
from scrap_tools import get_all_hrefs, scrap


def main():
    create_db()

    while True:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/109.0.5414.120 Safari/537.36 Avast/109.0.19987.120'

        }

        urls = get_all_hrefs(headers)

        scrap(urls, headers)

        check_sold_cars(urls)
        check_price_changes(headers, urls)

        break  # time.sleep(600)


if __name__ == '__main__':
    main()
