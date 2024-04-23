#!/usr/bin/python3
"""starts a Flask web application"""

from flask import Flask

app = Flask(__name__)


@app.route("/c/<text>", strict_slashes=False)
def custom_route(text):
    """Defining route (/hbnb)"""
    string = text.replace("_", " ")
    string = f"C {string}"
    return string


if __name__ == "__main__":
    app.run()
