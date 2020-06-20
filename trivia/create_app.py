from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from trivia import utils
from trivia.config import configs


def create_app(env=None):
    app = Flask(__name__)

    if not env:
        env = app.config['ENV']
    app.config.from_object(configs[env])

    # Setup a scheduler for automatically refreshing data
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(func=utils.refreshScores, trigger="interval", seconds=5)

    with app.app_context():
        utils.refreshScores()

    return app
