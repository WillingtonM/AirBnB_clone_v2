#!/usr/bin/python3
"""
    Place module for the HBNB project
"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
import models
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from os import environ

storage_engine = environ.get("HBNB_TYPE_STORAGE")

if storage_engine == "db":
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """
        Place class class
        
        Inherits from SQLAlchemy Base.

        Attributes:
            __tablename__ (str): The name of table to store places.
            city_id (String): The city id.
            user_id (String): The place's user id.
            name (String): The name of the place.
            description (String): Description of the place.
            number_rooms (Integer): Number of rooms of a place.
            number_bathrooms (Integer): Number of bathrooms in the place.
            max_guest (Integer): Maximum number of guests of the place.
            price_by_night (Integer): Price per night.
            latitude (Float): Latitude of the place .
            longitude (Float): Longitude of the place.
            reviews (relationship): Place-Review relationship.
            amenities (relationship): Place-Amenity relationship.
            amenity_ids (list): id list of all linked amenities.
    """
    __tablename__ = "places"
    if (storage_engine == "db"):
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
        reviews = relationship("Review", backref="place", cascade="delete")
        amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """get function for list of all linked Reviews"""
            rev_list = []
            rev_tmp = models.dummy_classes['Review']
            for rev in models.storage.all(rev_tmp).values():
                if rev.place_id == self.id:
                    rev_list.append(rev)
            return rev_list

        @property
        def amenities(self):
            """get function for linked Amenities"""
            amn_list = []
            amn_tmp = models.dummy_classes['Amenity']
            for amn in models.storage.all(amn_tmp).values():
                if amn in self.amenity_ids:
                    amn_list.append(amn)
            return amn_list

        @amenities.setter
        def amenities(self, obj):
            """ set function for linked Amenities"""
            amn_tmp = models.dummy_classes['Amenity']
            if (isinstance(obj, models.storage.all(amn_tmp))):
                self.amenity_ids.append(obj.id)