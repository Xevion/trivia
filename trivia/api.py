"""
api.py

Handles backend routes assisting
"""
import json

from flask import request, jsonify, make_response

from trivia import app
from trivia.utils import lastModified


@app.route("/api/changed")
@app.route("/api/changed/")
def changed():
    """
    A simple substitute for the 304 Not Modified HTTP return.

    :return True if data has changed since last

    TODO: Remove this function once a proper 304 Not Modified implementation is found for client side.
    """
    from trivia.utils import lastChange
    time = int(request.args.get('last') or lastModified())
    return jsonify(lastChange < time)


@app.route("/api/refresh")
@app.route("/api/refresh/")
def refresh():
    """
    Used for refreshing client-side table data. Returns a JSON response with all data necessary to build the table.
    """
    from trivia.utils import teams
    r = make_response(json.dumps([team._asdict() for team in teams]))
    print(r)
    r.mimetype = 'application/json'
    return r
