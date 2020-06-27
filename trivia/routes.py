"""
routes.py

Handles user frontend routes.
"""
from flask import render_template, current_app


@current_app.route("/")
def index():
    """
    Handles the frontend user index.

    :return:
    """
    from trivia.utils import teams
    scoreCount = max([len(team.scores) for team in teams]) if len(teams) > 0 else 0
    return render_template('index.html', scoreCount=scoreCount, teams=teams, title=current_app.config['APPLICATION_TITLE'])
