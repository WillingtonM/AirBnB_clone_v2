#!/usr/bin/python3
""" Amenity Class for HBNB project """
import os
from models.base_model import Base, BaseModel
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
        Amenity for database.

        Inherits from Base and links to table amenities.

        Attributes:
            __tablename__ (str): The name of table to store Amenities.
            name (String): Amenity name.
            place_amenities (relationship): Place-Amenity relationship.
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity")
