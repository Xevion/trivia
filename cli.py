"""
cli.py

A simple CLI implementation using the application's API.
"""

import curses
import random
import shutil
import string

from terminaltables import SingleTable

def generateTable() -> SingleTable:
    tableData = [team() for _ in range(5)]
    tableData.insert(0, ['Rank', 'ID', 'Team Name'] + list(map(str, range(1, 18))))
    return SingleTable(tableData)


def team():
    return [random.randint(1, 15), random.randint(1, 30), ''.join(random.choices(string.ascii_letters, k=18))] + [random.randint(0, 9) for _ in range(20)]


def main(stdscr):
    while True:
        y, x = stdscr.getmaxyx()
        stdscr.clear()

        # Print Table to screen
        table = generateTable()
        for i, stringRow in enumerate(table.table.split('\n')):
            stdscr.addstr(i, 0, stringRow[:x])
        stdscr.addstr(y - 1, 0, str((x, y)))
        # Check for quit key
        key = stdscr.getch()
        if key == ord('q'):
            break

        stdscr.refresh()


if __name__ == "__main__":
    screen = curses.initscr()
    try:
        curses.cbreak()
        screen.nodelay(1)
        curses.noecho()
        screen.keypad(True)
        main(screen)
    finally:
        screen.clear()
        curses.nocbreak()
        curses.echo()
        curses.endwin()