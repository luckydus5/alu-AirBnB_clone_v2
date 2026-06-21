#!/usr/bin/python3
"""Starts a Flask web app listing states and a single state's cities."""
from flask import Flask, render_template

from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_storage(exception):
    """Remove the current SQLAlchemy session after each request."""
    storage.close()


@app.route("/states", strict_slashes=False)
def states():
    """Render an HTML page listing all states sorted by name (A->Z)."""
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    return render_template("9-states.html", states=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Render the cities of the state matching id, or a not-found page."""
    state = storage.all(State).get("State.{}".format(id))
    return render_template("9-states.html", state=state, found=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
