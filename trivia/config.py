"""
config.py


"""

configs = {
    'production': 'trivia.config.Config',
    'productiondep': 'trivia.config.ConfigDeprecated',
    'development': 'trivia.config.Config',
    'demo': 'trivia.config.DemoConfig'
}


class Config(object):
    # Main Configuration
    APPLICATION_TITLE = 'EfTA Trivia Night'
    SCORE_FILE = 'scores.json'
    POLLING_INTERVAL = 5
    DEBUG = False
    CONVERT_OLD = True

    # Demo Configuration
    DEMO = False
    DEMO_TEAM_COUNT = 0
    DEMO_ALTERATION_INTERVAL = 0
    DEMO_MAX_SCORES = 0


class ConfigDeprecated(Config):
    CONVERT_OLD = True


class DemoConfig(Config):
    # Main Configuration
    SCORE_FILE = 'demo.json'
    DEBUG = True

    # Demo Configuration
    DEMO = True
    DEMO_TEAM_COUNT = 30
    DEMO_ALTERATION_INTERVAL = 3
    DEMO_MAX_SCORES = 20
