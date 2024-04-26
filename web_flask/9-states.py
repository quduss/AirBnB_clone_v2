#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /states_list: HTML page with a list of all State objects in DBStorage.
"""
from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states_list():
    """Displays an HTML page with a list of all State objects in DBStorage.

    The States are sorted by name.
    """
    states = storage.all(State)
    return render_template("9-states.html", states=states)


@app.route("/states/<id>", strict_slashes=False)
def state(id):
    """Displays an HTML page that lists the state with the given id
    . It also lists the cities in that state in a sorted manner. If
    the id provided doesn't link to a valid state, a 'Not Found'
    message is displayed"""
    key = f'State.{id}'
    if key in storage.all():
        obj = storage.all()[key]
    else:
        obj = None
    return render_template("9-states.html", obj=obj)


@app.teardown_appcontext
def teardown(exception=None):
    """Removes the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
