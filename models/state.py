#!/usr/bin/python3
"""Defines the State class that inherits from BaseModel and Base."""
from os import getenv

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """Represents a state where cities are located."""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship(
            "City", backref="state", cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """Return the list of City objects linked to the current State."""
            from models import storage
            return [city for city in storage.all(City).values()
                    if city.state_id == self.id]
