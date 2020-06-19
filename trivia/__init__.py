"""
__init__.py
"""
from collections import namedtuple

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

app = Flask(__name__)

# Simple fake 'class' for passing to jinja templates
Team = namedtuple('Team', ['id', 'name', 'scores'])

from trivia import routes, api, utils

# Setup a scheduler for automatically refreshing data
scheduler = BackgroundScheduler()
scheduler.add_job(func=utils.refreshScores, trigger="interval", seconds=5)

utils.refreshScores()

