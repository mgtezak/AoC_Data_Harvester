# Third Party
import pytz

# Native
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Puzzle:
    year: int
    day: int
    title: str | None = None

    @classmethod
    def from_today(cls):
        today = datetime.today()
        return cls(today.year, today.day)


def get_curr_max_date() -> tuple[int, int]:
    """Fetches the local time for advent of code (EST/UTC-5) and returns year and day of the latest puzzle."""

    curr = datetime.now(pytz.timezone('EST'))
    year, month, day = curr.year, curr.month, curr.day
    is_december = (month == 12)
    
    MAX_YEAR = year if is_december else year - 1
    MAX_DAY = day if is_december and day < 25 else 25
    return MAX_YEAR, MAX_DAY

MAX_YEAR, MAX_DAY = get_curr_max_date()