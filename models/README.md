# models

Data models and storage engines for the AirBnB clone.

- `base_model.py` — `BaseModel` and the SQLAlchemy declarative `Base`.
- `user.py`, `state.py`, `city.py`, `amenity.py`, `place.py`, `review.py` —
  the model classes, mapped to database tables with relationships.
- `engine/` — the `FileStorage` and `DBStorage` storage engines.
- `__init__.py` — instantiates the shared `storage` object, selecting the
  engine from the `HBNB_TYPE_STORAGE` environment variable.
