#!/usr/bin/python3
"""Models package; initializes the shared ``storage`` instance.

The storage engine is selected by the HBNB_TYPE_STORAGE environment
variable: ``db`` uses DBStorage (MySQL), anything else uses FileStorage.
"""
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
