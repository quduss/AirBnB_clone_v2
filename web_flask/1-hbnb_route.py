#!/usr/bin/python3
"""starts a Flask web application"""

from flask import Flask

app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Defining route (/hbnb)"""
    return "HBNB"


if __name__ == "__main__":
    app.run()
