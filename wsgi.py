"""
wsgi.py

Simple launcher file for project.
"""

from trivia import app

if __name__ == "__main__":
    app.run(host="0.0.0.0")