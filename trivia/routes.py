"""
routes.py

Handles user frontend routes.
"""

from trivia import app


@app.route("/")
def index():
    """
    Handles the frontend user index.

    :return:
    """
    return 'index'
