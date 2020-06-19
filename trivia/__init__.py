"""
__init__.py
"""

from flask import Flask

# initialize Flask object
app = Flask(__name__)

from trivia import routes, api
