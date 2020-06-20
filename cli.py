"""
cli.py

A simple CLI implementation using the application's API.
"""

import curses
from datetime import datetime
from typing import List

import pytz
import requests
from terminaltables import SingleTable

scores: List[dict] = []
lastAttempt: float = -1
lastUpdate: datetime = None


def refreshScores() -> None:
    global lastUpdate, lastAttempt, scores

    # Send with If-Modified-Since header if this is not the first time
    headers = {'If-Modified-Since': lastUpdate.strftime('%a, %d %b %Y %I:%M:%S %Z')} if lastUpdate else {}
    # Send request with headers
    resp = requests.get('http://localhost:5000/api/scores/', headers=headers)

    if resp.ok:
        if resp.status_code == 304 and len(scores) != 0:
            pass
        else:
            # Changes found, update!
            lastUpdate = datetime.now(pytz.utc)
            print(f'"{resp.text}"')
            scores = resp.json()


def main(screen):
    while True:
        # Get current terminal size and clear
        y, x = screen.getmaxyx()
        screen.clear()

        global scores
        # Print Table to screen
        table = [[-1, team['id'], team['name'], team['total'], *team['scores']] for team in scores[:y - 4]]
        table.insert(0, ['Rank', 'ID', 'Team Name', 'Total'])

        table = SingleTable(table)

        for i, stringRow in enumerate(table.table.split('\n')[:y]):
            screen.addstr(i, 0, stringRow[:x])
        screen.addstr(y - 1, 1, str((x, y)))

        # Check for quit key
        key = screen.getch()
        if key == ord('q'):
            break

        screen.refresh()


if __name__ == "__main__":
    stdscr = curses.initscr()
    # Setup curses friendly terminal flags, run app
    try:
        refreshScores()
        curses.cbreak()
        stdscr.nodelay(1)
        curses.noecho()
        curses.curs_set(False)
        stdscr.keypad(True)
        main(stdscr)
    # Undo curses terminal options
    finally:
        stdscr.clear()
        curses.nocbreak()
        curses.echo()
        curses.endwin()
