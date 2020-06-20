"""
api.py

Handles backend routes assisting
"""
import json
import time

from flask import request, make_response

from trivia import app


@app.route("/api/refresh")
@app.route("/api/refresh/")
def refresh():
    """
    Used for refreshing client-side table data. Returns a JSON response with all data necessary to build the table.
    """
    from trivia.utils import teams, lastChange

    # Create response using namedtuples
    r = make_response(json.dumps([team._asdict() for team in teams]))
    r.mimetype = 'application/json'

    status_code = 200
    # Try to handle If-Modified-Since header properly (304 Not Modified
    try:
        if request.headers['If-Modified-Since']:
            # Acquire epoch time from header
            epoch = time.mktime(time.strptime(request.headers['If-Modified-Since'], "%a, %d %b %Y %I:%M:%S %Z"))
            if epoch < lastChange:
                status_code = 304
    except KeyError:
        pass  # Header was not supplied. Ignore.
    except ValueError:
        print('If-Modified-Since Header could not be parsed.')  # Header could not be parsed.

    return r, status_code
