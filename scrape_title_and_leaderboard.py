# Third Party
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame 

# Native
import time

# Local
from puzzle import Puzzle
from config import REQUEST_HEADER
from db import insert_puzzle_into_db, insert_leaderboard_into_db


def main() -> None:
    puzzle = Puzzle.from_today()

    scrape_title(puzzle)
    time.sleep(900)   # throttle requests to comply with guidelines
    leaderboard = scrape_leaderboard(puzzle)

    insert_puzzle_into_db(puzzle)
    insert_leaderboard_into_db(leaderboard)


def scrape_title(puzzle: Puzzle) -> None:
    url = f'https://adventofcode.com/{puzzle.year}/day/{puzzle.day}'
    response = requests.get(url, headers=REQUEST_HEADER)
    soup = BeautifulSoup(response.text, 'html.parser')
    puzzle.title = soup.h2.text.split(':', maxsplit=1)[1].strip('- ')


def convert_to_seconds(hh_mm_ss: str) -> int:
    hours, minutes, seconds = map(int, hh_mm_ss.split(':'))
    return 3600 * hours + 60 * minutes + seconds


def scrape_leaderboard(puzzle: Puzzle) -> DataFrame:
    url = f'https://adventofcode.com/{puzzle.year}/leaderboard/day/{puzzle.day}'
    response = requests.get(url, headers=REQUEST_HEADER)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    for i, div in enumerate(soup.main.find_all('div')):
        line = div.text

        part = 2 if i < 100 else 1
        rank = i % 100 + 1
        seconds = convert_to_seconds(line[13:21])

        is_sponsor = '(Sponsor)' in line
        is_supporter = '(AoC++)' in line

        if is_sponsor and is_supporter:
            name = line[22:-18]
        elif is_sponsor:
            name = line[22:-10]
        elif is_supporter:
            name = line[22:-8]
        else:
            name = line[22:]

        data.append((puzzle.year, puzzle.day, part, rank, seconds, name, is_supporter, is_sponsor))

    columns = ['year', 'day', 'part', 'rank', 'seconds', 'name', 'is_supporter', 'is_sponsor']
    return DataFrame(data, columns=columns)


if __name__ == '__main__':
    main()
