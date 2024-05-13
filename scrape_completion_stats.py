# Third party
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Native
import time
import re
from datetime import date

# Local
from config import REQUEST_HEADER, MAX_EVENT_YEAR
from db import insert_stats_into_db


def main():
    stats = scrape_stats()
    insert_stats_into_db(stats)


def scrape_stats() -> None:

    timestamp = str(date.today())
    data = []
    columns = ['timestamp', 'year', 'day', 'gold', 'silver']

    for year in range(2015, MAX_EVENT_YEAR+1):

        if year > 2015:
            time.sleep(900)   # throttle requests to comply with guidelines

        url = f'https://adventofcode.com/{year}/stats'
        page = requests.get(url, headers=REQUEST_HEADER)
        soup = BeautifulSoup(page.content, 'html.parser')
        year_stats = soup.find(class_='stats').text
        year_stats_lines = re.findall('(\d+)\s+(\d+)\s+(\d+)', year_stats)

        for day_stats in reversed(year_stats_lines):
            day, gold, silver = map(int, day_stats)
            data.append((timestamp, year, day, gold, silver))

    return pd.DataFrame(data=data, columns=columns)


if __name__ == '__main__':
    main()
