#!/usr/bin/python3
"""Starts a Flask web application listing all State objects from storage."""
from flask import Flask, render_template

from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_storage(exception):
    """Remove the current SQLAlchemy session after each request."""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Render an HTML page with all states sorted by name (A->Z)."""
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
