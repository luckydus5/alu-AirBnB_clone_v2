#!/usr/bin/python3
"""Defines the FileStorage class for JSON-file-backed object persistence."""
import json


class FileStorage:
    """Serializes instances to a JSON file and deserializes them back.

    Private class attributes:
        __file_path: path to the JSON file where objects are persisted.
        __objects: dictionary of stored objects keyed by ``<class name>.id``.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return the dictionary __objects, optionally filtered by class.

        When cls is provided, return only the objects of that class.
        """
        if cls is None:
            return FileStorage.__objects
        if isinstance(cls, str):
            cls_name = cls
        else:
            cls_name = cls.__name__
        return {key: obj for key, obj in FileStorage.__objects.items()
                if type(obj).__name__ == cls_name}

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file (path: __file_path)."""
        serializable = {}
        for key, obj in FileStorage.__objects.items():
            serializable[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(serializable, f)

    def reload(self):
        """Deserialize the JSON file to __objects, if the file exists.

        If the JSON file does not exist, do nothing and raise no exception.
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        for key, value in data.items():
            cls_name = value.get("__class__")
            if cls_name in classes:
                FileStorage.__objects[key] = classes[cls_name](**value)

    def delete(self, obj=None):
        """Delete obj from __objects if it is present; do nothing if None."""
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects.pop(key, None)

    def close(self):
        """Call reload() to deserialize the JSON file back to objects."""
        self.reload()
