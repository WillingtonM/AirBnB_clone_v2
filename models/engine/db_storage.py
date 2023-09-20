#!/usr/bin/python3
""" Db storage """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """ class dbstorage """
    __engine = None
    __session = None

    def __init__(self):
        """ a function that initialise class DBStorage"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        e = getenv("HBNB_ENV", "none")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, password, host, db),
                                      pool_pre_ping=True)
        if e == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ a function that returns a dictionary of
            objects in the current session
        """
        dic = {}
        if cls is None:
            classes = [State, City]  # add User, Place, Review, Amenity after
        elif isinstance(cls, str):
            try:
                cls = eval(cls)
                classes = [cls]
            except NameError:
                # Handle the case where cls is not a valid class name
                return dic
        elif isinstance(cls, type):
            classes = [cls]
        else:
            raise ValueError("Invalid cls argument. Expected\
                             class name or class type.")

        for cls in classes:
            q = self.__session.query(cls)
            dic.update({"{}.{}".format(type(obj).__name__, obj.id):
                        obj for obj in q})
        return dic

    def new(self, obj):
        """ adds objects to the current session"""
        self.__session.add(obj)

    def save(self):
        """updates the database with the current changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object in a session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ adds all object in a database to a session"""
        Base.metadata.create_all(self.__engine)
        s_f = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(s_f)
        self.__session = Session()
