# web_flask

Flask web application for the AirBnB clone (tasks 0-10).

Each task is a standalone module run with `python3 -m web_flask.<module>`,
for example `python3 -m web_flask.10-hbnb_filters`. The data-driven tasks
fetch from the active storage engine via `from models import storage` and
remove the SQLAlchemy session after every request with
`@app.teardown_appcontext`.

- `*.py` — the route definitions for each task.
- `templates/` — Jinja templates rendered by the routes.
- `static/` — CSS and images served for the `/hbnb_filters` page.
