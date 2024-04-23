#!/usr/bin/python3
"""starts a Flask web application"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """Defining route /"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Defining route /hbnb"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_is_text(text):
    """Defining route /c/<text>"""
    string = text.replace("_", " ")
    string = f"C {string}"
    return string


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_is_text(text="is cool"):
    """Defining route /python and /python/<text>"""
    string = text.replace("_", " ")
    string = f"Python {string}"
    return string


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """Defining route /number/<n> where n must be an integer"""
    return f'{n} is a number'


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Defining route /number_template/<n> where n must be an integer"""
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run()
