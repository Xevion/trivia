"""
utils.py

Stores important backend application functionality.
"""
import json
import os
import time
import random
from collections import namedtuple
from typing import List

# Simple fake 'class' for passing to jinja templates
import faker as faker
from flask import current_app

Team = namedtuple('Team', ['id', 'name', 'scores'])

# Generate paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SCORES_FILE = os.path.join(DATA_DIR, current_app.config['SCORE_FILE'])

# Initialize global data/tracking vars
lastChange: float = -1
teams: List[Team] = []


def lastModified() -> float:
    """
    returns epoch time of last modification to the scores file.
    """
    return os.stat(SCORES_FILE).st_mtime


def refreshScores() -> None:
    """
    Refreshes scores data safely.

    :return:
    """

    global lastChange
    curChange = lastModified()

    from trivia.create_app import scheduler
    app = scheduler.app

    with app.app_context():
        if lastChange < curChange:
            try:
                # Update tracking var
                lastChange = curChange

                current_app.logger.debug('Attempting to load and parse scores file.')
                with open(SCORES_FILE, 'r') as file:
                    temp = json.load(file)

                # Place all values into Team object for jinja
                temp = [
                    Team(
                        id=team['teamno'],
                        name=team['teamname'],
                        scores=team['scores']
                    ) for team in temp
                ]
                current_app.logger.debug(f'Successfully loaded ({len(temp)} teams).')

                global teams
                teams = temp

            # If invalid or inaccessible, simply do nothing.
            except json.JSONDecodeError:
                current_app.logger.error('Scores file could not be opened or parsed.', exc_info=True)


def generateDemo() -> None:
    fake = faker.Faker()
    data = [
        {
            'teamno': i + 1,
            'teamname': fake.user_name(),
            'scores': []
        } for i in range(current_app.config['DEMO_TEAM_COUNT'])
    ]

    with open(SCORES_FILE, 'w') as file:
        json.dump(data, file)


def alterDemo() -> None:
    from trivia.create_app import scheduler
    app = scheduler.app

    with app.app_context():
        current_app.logger.debug('Altering Demo Data...')
        with open(SCORES_FILE, 'r') as file:
            data = json.load(file)

        if len(data) > 0:
            if len(data[0]['scores']) >= current_app.config['DEMO_MAX_SCORES']:
                generateDemo()
            else:
                for team in data:
                    team['scores'].append(random.randint(2, 8) if random.random() > 0.25 else 0)

                with open(SCORES_FILE, 'w') as file:
                    json.dump(data, file)
