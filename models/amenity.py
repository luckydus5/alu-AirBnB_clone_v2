#!/usr/bin/python3
"""Defines the Amenity class that inherits from BaseModel and Base."""
from os import getenv

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Represents an amenity that a place can offer."""

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_amenities = relationship(
            "Place", secondary="place_amenity", viewonly=False,
            back_populates="amenities")
