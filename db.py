# Third Party
import pandas as pd
from pandas import DataFrame

# Native
from IPython.display import display
from dataclasses import asdict
import sqlite3

# Local
from base import Puzzle


# Config
DB = 'aoc.db'


# Create table
def create_stats_table_if_not_exists(year: str):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS stats{year} (
                timestamp TEXT NOT NULL, 
                year INTEGER NOT NULL, 
                day INTEGER NOT NULL, 
                gold INTEGER NOT NULL, 
                silver INTEGER NOT NULL,
                PRIMARY KEY (date, year, day),
                FOREIGN KEY (year, day) REFERENCES puzzles(year, day)
            );
        """)


# Insert data
def insert_puzzle_into_db(puzzle: Puzzle) -> None:
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO puzzles (year, day, title) VALUES (:year, :day, :title)', asdict(puzzle))


def insert_leaderboard_into_db(leaderboard: DataFrame):
    with sqlite3.connect(DB) as conn:
        leaderboard.to_sql('leaderboard', conn, if_exists='append', index=False)


def insert_stats_into_db(time_slice: DataFrame):
    record_year: str = time_slice.loc[0, 'timestamp'][:4]
    create_stats_table_if_not_exists(record_year)
    with sqlite3.connect(DB) as conn:
        time_slice.to_sql(f'stats{record_year}', conn, if_exists='append', index=False)


# Get data
def get_puzzles_table_from_db():
    with sqlite3.connect('aoc.db') as conn:
        return pd.read_sql_query('SELECT * FROM puzzles', conn)


def get_puzzle_from_db(year, day):
    with sqlite3.connect('aoc.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM puzzles WHERE year = {year} AND day = {day}")
        return Puzzle(*cursor.fetchone())


def get_leaderboard_table_from_db():
    with sqlite3.connect('aoc.db') as conn:
        return pd.read_sql_query('SELECT * FROM leaderboard', conn)


def get_puzzle_leaderboard_from_db(year, day):
    with sqlite3.connect('aoc.db') as conn:
        query = f'SELECT * FROM leaderboard WHERE year = {year} AND day = {day}'
        return pd.read_sql_query(query, conn)


def get_stats_table_from_db():
    with sqlite3.connect('aoc.db') as conn:
        return pd.read_sql_query('SELECT * FROM stats2024', conn)


def get_db_metadata():
    with sqlite3.connect('aoc.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Tables in the database:")
        meta_columns = ['', 'column name', 'data type', 'not null', 'default value', 'primary key']
        for table in tables:
            row_count = cursor.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
            columns = cursor.execute(f"PRAGMA table_info('{table[0]}')").fetchall()
            print(f'\n{table[0]} – {row_count} rows')  
            display(pd.DataFrame(columns, columns=meta_columns).drop('', axis=1))          


# Delete data
def delete_puzzle_from_db(puzzle: Puzzle) -> None:
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM puzzles WHERE year = :year AND day = :day', asdict(puzzle))
        

def delete_stats_timestamp_from_db(timestamp):
    record_year = timestamp[:4]
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM stats{record_year} WHERE timestamp = '{timestamp}'")
