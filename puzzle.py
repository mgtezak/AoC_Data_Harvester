# Native
from dataclasses import dataclass
from datetime import date


@dataclass
class Puzzle:
    year: int
    day: int
    title: str | None = None

    @classmethod
    def from_today(cls):
        today = date.today()
        return cls(today.year, today.day)
    