# Advent of Code automated web scraping bots

This repo contains the scripts for two automated bots, which run at different times and collect different types of data. Both are configured to comply with [Advent of Code's web scraping guidelines](https://old.reddit.com/r/adventofcode/wiki/faqs/automation/).
1. there are no redundant requests
2. requests are separated by 900 seconds or 15 minutes
3. each request includes a header linking back to this public repo

## #1: Puzzle title and leaderboard scraper

- Runs only during the event
- Cron expression: `0 7 1-25 12 *` (7am UTC = 2 hours after puzzle release, every day from 1st - 25th December)
- Two requests in total:
    - One for today's puzzle title
    - One for the public leaderboard
- Collected data is inserted into the `puzzles` & `leaderboard` tables

## #2: Completion stats scraper

- Runs daily at noon UTC
- Cron expression: `0 12 * * *`
- Number of requests: 1 for each past event (currently 2024 - 2015 = 9)
- Collects the Gold & Silver completions for each day of each year
- Collected data is inserted into the current year's stats table (e.g. `stats2024`)
