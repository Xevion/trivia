"""
utils.py

Stores important backend application functionality.
"""
import os
import json

from typing import List
from trivia import Team

# Generate paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

data: List[Team] = None


def refresh() -> None:
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
                rank=-1,
                id=team['teamno'],
                name=team['teamname'],
                scores=team['scores']
            ) for team in temp
        ]
        print(f'Successfully loaded ({len(temp)} teams).')
        data = temp
    # If invalid or inaccessible, simply do nothing.
    except json.JSONDecodeError:
        print('Scores file could not be opened or parsed.')