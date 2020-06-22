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
lastUpdate: float = -1


def refreshScores() -> None:
    """
    Refreshes scoreboard data safely, handling a unresponsive or downed scoreboard.
    Uses If-Modified-Since headers properly.
    Modifies lastAttempt, lastUpdate and scores global vars to track and store data.

    :return: True if Score data has been updated.
    """

    global lastUpdate, lastAttempt, scores

    # Send with If-Modified-Since header if this is not the first time
    useTime = max(lastAttempt, lastUpdate)
    headers = {
        'If-Modified-Since': datetime.fromtimestamp(useTime, pytz.utc).strftime(
            '%a, %d %b %Y %I:%M:%S %Z')} if useTime > 0 else {}
    # Send request with headers
    try:
        resp = requests.get('http://127.0.0.1:5000/api/scores/', headers=headers)
    except requests.exceptions.ConnectionError:
        resp = None
    finally:
        lastAttempt = datetime.utcnow().timestamp()

    if resp is not None and resp.ok:
        if resp.status_code == 304 and len(scores) != 0:
            pass
        else:
            # Changes found, update!
            lastUpdate = datetime.utcnow().timestamp()
            scores = resp.json()

            # Calculate totals, preliminary sort by total
            for team in scores:
                team['total'] = sum(team['scores'])
            scores.sort(key=lambda team: team['total'], reverse=True)

            # Calculate ranks with tie handling logic
            for i, team in enumerate(scores):
                # Check that previous score is the same, if so add a 'T' for tie
                if i > 0 and scores[i - 1]['total'] == team['total']:
                    team['rank'] = scores[i - 1]['rank']

                    # Check if we have a T
                    if not team['rank'].startswith('T'):
                        team['rank'] = 'T' + team['rank'].strip()

                    # Check if previous score has a T
                    if not scores[i - 1]['rank'].startswith('T'):
                        scores[i - 1]['rank'] = 'T' + scores[i - 1]['rank'].strip()
                else:
                    # Otherwise just add a space in front instead
                    team['rank'] = " " + str(i + 1)


def main(screen) -> None:
    """
    Mainloop function.

    :param screen: Curses screen
    """

    screen.redrawwin()
    while True:
        # Refresh scores every 10 seconds
        if datetime.utcnow().timestamp() - lastAttempt > 0.5:
            refreshScores()

        # Get current terminal size and clear
        y, x = screen.getmaxyx()
        screen.clear()

        # Build table data
        global scores
        table = [[team['rank'], team['id'], team['name'], team['total'], *team['scores']] for team in scores[:y - 4]]
        # Round number headers
        scoreSet = map(str, range(1, max(8, len(scores[0]['scores'])) + 1)) if scores else []
        table.insert(0, ['Rank', 'ID', 'Team Name', 'T', *scoreSet])
        table = SingleTable(table, title='EfTA Trivia Night')

        for row in table.table_data:
            pass

        # Show Table
        for i, stringRow in enumerate(table.table.split('\n')[:y]):
            screen.addstr(i, 0, stringRow[:x])

        # Terminal Size
        strpos = str((x, y))
        screen.addstr(y - 1, 1, strpos)
        screen.addstr(y - 1, 1 + len(strpos) + 1,
                      f'({str(round(0.5 - (datetime.utcnow().timestamp() - lastAttempt), 3)).zfill(3)})')

        # Update curses screen
        screen.refresh()

        # Check for quit key
        key = screen.getch()
        if key == ord('q'):
            break


if __name__ == "__main__":
    stdscr = curses.initscr()
    # Setup curses friendly terminal flags, run app
    try:
        curses.cbreak()
        stdscr.nodelay(1)
        curses.noecho()
        curses.curs_set(False)
        stdscr.keypad(True)
        refreshScores()
        main(stdscr)
    # Undo curses terminal options
    finally:
        stdscr.clear()
        curses.nocbreak()
        curses.echo()
        curses.endwin()
