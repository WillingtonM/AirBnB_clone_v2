#!/usr/bin/python3
""" holds class User"""
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
        Represents a user database.

        Inherits from Base and links to table users.

        Attributes:
            __tablename__ (str): Name table to store users.
            email: (String): User's email address.
            password (String): User's password.
            first_name (String): User's first name.
            last_name (String): The user's last name.
            places (relationship): User-Place relationship.
            reviews (relationship): The User-Review relationship.
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship("Place", backref="user", cascade="delete")
    reviews = relationship("Review", backref="user", cascade="delete")
