#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage"""
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


st = getenv("HBNB_TYPE_STORAGE")
if st == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()
storage.reload()
