#!/usr/bin/python3
"""Defines the BaseModel class, the base for all AirBnB clone models."""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """Base class defining common attributes and methods for all models."""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.

        When kwargs is provided, rebuild the instance from its dictionary
        representation. Otherwise create a brand new instance with a unique
        id and current timestamps.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ("created_at", "updated_at") and isinstance(
                        value, str):
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __str__(self):
        """Return the string representation of the BaseModel instance."""
        attrs = {key: value for key, value in self.__dict__.items()
                 if key != "_sa_instance_state"}
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, attrs)

    def save(self):
        """Update updated_at with the current datetime and persist storage."""
        self.updated_at = datetime.now()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance.

        Adds a __class__ key with the class name, converts datetimes to ISO
        format strings, and removes the SQLAlchemy internal state key.
        """
        result = self.__dict__.copy()
        result["__class__"] = self.__class__.__name__
        if isinstance(result.get("created_at"), datetime):
            result["created_at"] = self.created_at.isoformat()
        if isinstance(result.get("updated_at"), datetime):
            result["updated_at"] = self.updated_at.isoformat()
        result.pop("_sa_instance_state", None)
        return result

    def delete(self):
        """Delete the current instance from storage."""
        from models import storage
        storage.delete(self)
