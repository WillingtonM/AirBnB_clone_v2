#!/usr/bin/python
"""
    Review module for the HBNB project
"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """
        Represents a review for a MySQL database.

        Inherits from Base and links to table reviews.

        Attributes:
            __tablename__ (str): Name of table to store Reviews.
            text (String): Review description.
            place_id (String): Review's place id.
            user_id (String): Review's user id.
    """
    __tablename__ = "reviews"
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)
