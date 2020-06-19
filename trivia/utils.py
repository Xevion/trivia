"""
utils.py

Stores important backend application functionality.
"""
import json
import os

from trivia import Team

# Generate paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# data: List[Team] = []
teams = []


def refreshScores() -> None:
    """
    Refreshes scores data safely.

    :return:
    """

    try:
        print('Attempting to load and parse scores file.')
        with open(os.path.join(DATA_DIR, 'scores.json')) as file:
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
