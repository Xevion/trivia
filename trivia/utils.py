"""
utils.py

Stores important backend application functionality.
"""
import json
import os
import random
import time
from collections import namedtuple
from datetime import datetime
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
    if current_app.config['DEBUG']:
        print(datetime.fromtimestamp(os.path.getmtime(SCORES_FILE)), datetime.fromtimestamp(time.time()))
    return os.path.getmtime(SCORES_FILE)


def refreshScores() -> None:
    """
    Refreshes scores data safely.
    """

    from trivia.create_app import scheduler
    app = scheduler.app
    with app.app_context():
        global lastChange
        curChange = lastModified()

        if lastChange < curChange:
            try:
                # Update tracking var
                lastChange = curChange

                current_app.logger.debug('Attempting to load and parse scores file.')
                with open(SCORES_FILE, 'r') as file:
                    temp = json.load(file)
                    if current_app.config['CONVERT_OLD']:
                        temp = convertFrom(temp)

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
    """
    Generate a base demo scores file. Overwrites the given SCORES_FILE.
    """

    fake = faker.Faker()
    data = [
        {
            'teamno': i + 1,
            'teamname': fake.user_name(),
            'scores': []
        } for i in range(current_app.config['DEMO_TEAM_COUNT'])
    ]

    with open(SCORES_FILE, 'w') as file:
        json.dump(convertTo(data) if current_app.config['CONVERT_OLD'] else data, file)


def alterDemo() -> None:
    """
    Alters the current scores file. Intended for demo application mode.
    Adds a new score each alteration. Triggers a application fresh with 'refreshScores'
    """

    from trivia.create_app import scheduler
    app = scheduler.app

    with app.app_context():
        current_app.logger.debug('Altering Demo Data...')
        with open(SCORES_FILE, 'r') as file:
            data = convertFrom(json.load(file)) if current_app.config['CONVERT_OLD'] else json.load(file)

        if len(data) > 0:
            if len(data[0]['scores']) >= current_app.config['DEMO_MAX_SCORES']:
                generateDemo()
            else:
                for team in data:
                    team['scores'].append(random.randint(2, 8) if random.random() > 0.25 else 0)

                with open(SCORES_FILE, 'w') as file:
                    json.dump(convertTo(data) if current_app.config['CONVERT_OLD'] else data, file)

                refreshScores()


def convertFrom(data) -> List[dict]:
    """
    Converts scores data from old to new format.

    :param data: Old format data
    :return: Old format data
    """
    return [
        {
            'teamno': oldteam['Team']['Number'],
            'teamname': oldteam['Team']['DisplayName'],
            'scores': oldteam['Scores']
        }
        for oldteam in data
    ]


def convertTo(data) -> List[dict]:
    """
    Converst scores from new to old format
    :param data: New format data
    :return: Old format data
    """
    return [
        {
            'Team': {
                'Number': team['teamno'],
                'DisplayName': team['teamname']
            },
            'Scores': team['scores'],
            'TotalGuess': -1
        } for team in data
    ]
