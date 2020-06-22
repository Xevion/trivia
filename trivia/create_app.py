from flask import Flask
from flask_apscheduler import APScheduler

from trivia.config import configs

scheduler: APScheduler = None


def create_app(env=None):
    app = Flask(__name__)

    if not env:
        env = app.config['ENV']
    app.config.from_object(configs[env])

    with app.app_context():
        # noinspection PyUnresolvedReferences
        from trivia import routes, api, utils

        # Setup a scheduler for automatically refreshing data
        global scheduler
        scheduler = APScheduler()
        scheduler.init_app(app)
        scheduler.start()

        # Add score file polling
        scheduler.add_job(id='polling', func=utils.refreshScores, trigger="interval",
                          seconds=app.config['POLLING_INTERVAL'])

        if app.config['DEMO']:
            app.logger.info('Generating Demo Data...')
            # Generate initial Demo data
            utils.generateDemo()
            # Begin altering demo data regularly
            scheduler.add_job(id='altering', func=utils.alterDemo, trigger="interval",
                              seconds=app.config['DEMO_ALTERATION_INTERVAL'])

        utils.refreshScores()

    return app
