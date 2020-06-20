"""
config.py


"""

configs = {
    'production': 'trivia.config.Config',
    'development': 'trivia.config.Config',
    'demo': 'trivia.config.DemoConfig'
}


class Config(object):
    SCORE_FILE = 'scores.json'
    DEMO = False



class DemoConfig(Config):
    SCORE_FILE = 'demo.json'
    DEMO = True
