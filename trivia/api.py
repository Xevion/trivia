"""
api.py

Handles backend routes assisting
"""
from flask import request

from trivia import app


@app.route("/api/changed")
@app.route("/api/changed/")
def changed():
    """
    A simple substitute for the 304 Not Modified HTTP return.

    :return True if data has changed since last

    TODO: Remove this function once a proper 304 Not Modified implementation is found for client side.
    """

    time = request.args.get('last')


@app.route("/api/refresh")
@app.route("/api/refresh/")
def refresh():
    """
    Used for refreshing client-side table data. Returns a JSON response with all data necessary to build the table.
    """
