# models/engine

Storage engines that persist the AirBnB clone objects.

- `file_storage.py` — `FileStorage`: serializes objects to a JSON file
  (`file.json`) and deserializes them back. Includes `close()`.
- `db_storage.py` — `DBStorage`: stores objects in a MySQL database via
  the SQLAlchemy ORM. Includes `close()` to remove the current session.

The active engine is chosen in `models/__init__.py` based on the
`HBNB_TYPE_STORAGE` environment variable (`db` for DBStorage, otherwise
FileStorage).
