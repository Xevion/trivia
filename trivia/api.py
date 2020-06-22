"""
api.py

Handles backend routes assisting
"""
import json
import time

from datetime import datetime
from flask import request, make_response, current_app


@current_app.route("/api/scores")
@current_app.route("/api/scores/")
def scores():
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
            if current_app.config['DEBUG']:
                print(request.headers['If-Modified-Since'])
            epoch = datetime.strptime(request.headers['If-Modified-Since'], "%a, %d %b %Y %I:%M:%S %Z")
            if current_app.config['DEBUG']:
                print(epoch)
            epoch = epoch.timestamp()
            if current_app.config['DEBUG']:
                print(epoch, lastChange, lastChange - epoch)
            if epoch >= lastChange:
                status_code = 304
    except KeyError:
        pass  # Header was not supplied. Ignore.
    except ValueError:
        current_app.logger.warning('If-Modified-Since Header could not be parsed.', exc_info=True)  # Header could not be parsed.

    return r, status_code
