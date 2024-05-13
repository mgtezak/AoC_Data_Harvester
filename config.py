from datetime import date

DB_PATH = 'aoc.db'
REQUEST_HEADER = {'Bot-Alert': 'github.com/mgtezak/aoc_data_harvester by mgtezak@gmail.com'}

today = date.today()
MAX_EVENT_YEAR = today.year if today.month == 12 else today.year - 1