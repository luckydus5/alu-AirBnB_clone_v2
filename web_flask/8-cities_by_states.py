#!/usr/bin/python3
"""Starts a Flask web application listing states with their cities."""
from flask import Flask, render_template

from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_storage(exception):
    """Remove the current SQLAlchemy session after each request."""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """Render an HTML page listing each state and its cities, A->Z."""
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
