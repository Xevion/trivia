"""
utils.py

Stores important backend application functionality.
"""
import json
import os
from typing import List

from trivia import Team

# Generate paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Initialize global data/tracking vars
lastChange: int = -1
teams: List[Team] = []


def refreshScores() -> None:
    """
    Refreshes scores data safely.

    :return:
    """

    global lastChange
    filepath = os.path.join(DATA_DIR, 'scores.json')
    curChange = os.stat(filepath).st_mtime

    if lastChange < curChange:
        try:
            # Update tracking var
            lastChange = curChange

            print('Attempting to load and parse scores file.')
            with open(filepath) as file:
                temp = json.load(file)

            # Place all values into Team object for jinja
            temp = [
                Team(
                    id=team['teamno'],
                    name=team['teamname'],
                    scores=team['scores']
                ) for team in temp
            ]
            print(f'Successfully loaded ({len(temp)} teams).')

            global teams
            teams = temp

        # If invalid or inaccessible, simply do nothing.
        except json.JSONDecodeError:
            print('Scores file could not be opened or parsed.')
