#!/usr/bin/python3
"""
    Place module for the HBNB project
"""
import models
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import Column, Float, Integer, ForeignKey, String, Table
from sqlalchemy.orm import relationship


association_table = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True,
                                 nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """
        Place class class

        Inherits from SQLAlchemy Base.

        Attributes:
            __tablename__ (str): Name of table to store places.
            city_id (String): The city id.
            user_id (String): The place's user id.
            name (String): Name of place.
            description (String): Description of place.
            number_rooms (Integer): Number of rooms of a place.
            number_bathrooms (Integer): Number of bathrooms in place.
            max_guest (Integer): Maximum number of guests of place.
            price_by_night (Integer): Price per night.
            latitude (Float): Latitude of place .
            longitude (Float): Longitude of place.
            reviews (relationship): Place-Review relationship.
            amenities (relationship): Place-Amenity relationship.
            amenity_ids (list): id list of linked amenities.
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Get list of linked Reviews."""
            rev_ls = []
            for rev in list(models.storage.all(Review).values()):
                if rev.place_id == self.id:
                    rev_ls.append(rev)
            return rev_ls

        @property
        def amenities(self):
            """Get or set linked Amenities"""
            amn_ls = []
            for amn in list(models.storage.all(Amenity).values()):
                if amn.id in self.amenity_ids:
                    amn_ls.append(amn)
            return amn_ls

        @amenities.setter
        def amenities(self, value):
            if type(value) is Amenity:
                self.amenity_ids.append(value.id)
