from datetime import datetime

DB_PATH = 'aoc.db'
REQUEST_HEADER = {'Bot-Alert': 'github.com/mgtezak/aoc_data_harvester by mgtezak@gmail.com'}

today = datetime.today()
year, month = today.year, today.month
MAX_EVENT_YEAR = year if month == 12 else year - 1