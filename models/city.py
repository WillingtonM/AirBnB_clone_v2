#!/usr/bin/python
"""
    City module for the HBNB project
"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """
        City model for database.

        Inherits from Base and links to table cities.

        Attributes:
            __tablename__ (str): Name of table to store Cities.
            name (sqlalchemy String): Name of City.
            state_id (sqlalchemy String): State id of City.
    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    places = relationship("Place", backref="cities", cascade="delete")
