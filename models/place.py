#!/usr/bin/python3
"""Defines the Place class that inherits from BaseModel and Base."""
from os import getenv

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"),
           primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"),
           primary_key=True, nullable=False),
)


class Place(BaseModel, Base):
    """Represents a place (rental) listed on the AirBnB clone."""

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review", backref="place", cascade="all, delete")
        amenities = relationship(
            "Amenity", secondary=place_amenity, viewonly=False,
            back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            """Return the list of Review objects linked to this Place."""
            from models import storage
            from models.review import Review
            return [rev for rev in storage.all(Review).values()
                    if rev.place_id == self.id]

        @property
        def amenities(self):
            """Return the list of Amenity objects linked to this Place."""
            from models import storage
            from models.amenity import Amenity
            return [am for am in storage.all(Amenity).values()
                    if am.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Append an Amenity id to amenity_ids when given an Amenity."""
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
