#!/usr/bin/python3
"""Defines unnittests for models/review.py."""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class TestReview(unittest.TestCase):
    """Unittests for Test the Review class."""

    @classmethod
    def setUpClass(cls):
        """Review Test setup.
        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates FileStorage, DBStorage and Review instances for Test.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)
        cls.user = User(email="poppy@holberton.com", password="betty98")
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                          name="Betty")
        cls.review = Review(text="stellar", place_id=cls.place.id,
                            user_id=cls.user.id)

        if type(models.storage) is DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """Review Test teardown.
        Restore original file.json.
        Delete the FileStorage, DBStorage and Review instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.state
        del cls.city
        del cls.user
        del cls.place
        del cls.review
        del cls.filestorage
        if type(models.storage) is DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_func_pep8(self):
        """pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/review.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_func_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Review.__doc__)

    def test_func_attributes(self):
        """Check for attributes."""
        us = Review(email="a", password="a")
        self.assertEqual(str, type(us.id))
        self.assertEqual(datetime, type(us.created_at))
        self.assertEqual(datetime, type(us.updated_at))
        self.assertTrue(hasattr(us, "__tablename__"))
        self.assertTrue(hasattr(us, "text"))
        self.assertTrue(hasattr(us, "place_id"))
        self.assertTrue(hasattr(us, "user_id"))

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Test FileStorage")
    def test_func_nullable_attributes(self):
        """email attribute is non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Review(
                place_id=self.place.id, user_id=self.user.id))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Review(
                text="a", user_id=self.user.id))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Review(
                text="a", place_id=self.place.id))
            self.dbstorage._DBStorage__session.commit()

    def test_func_is_subclass(self):
        """Check Review is a subclass of BaseModel."""
        self.assertTrue(issubclass(Review, BaseModel))

    def test_func_two_models_are_unique(self):
        """different Review instances are unique."""
        us = Review(email="a", password="a")
        self.assertNotEqual(self.review.id, us.id)
        self.assertLess(self.review.created_at, us.created_at)
        self.assertLess(self.review.updated_at, us.updated_at)

    def test_func_init(self):
        """initialization."""
        self.assertIsInstance(self.review, Review)

    def test_func_str(self):
        """__str__ representation."""
        tst_st = self.review.__str__()
        self.assertIn("[Review] ({})".format(self.review.id), tst_st)
        self.assertIn("'id': '{}'".format(self.review.id), tst_st)
        self.assertIn("'created_at': {}".format(
            repr(self.review.created_at)), tst_st)
        self.assertIn("'updated_at': {}".format(
            repr(self.review.updated_at)), tst_st)
        self.assertIn("'text': '{}'".format(self.review.text), tst_st)
        self.assertIn("'place_id': '{}'".format(self.review.place_id), tst_st)
        self.assertIn("'user_id': '{}'".format(self.review.user_id), tst_st)

    def test_func_init_args_kwargs(self):
        """initialization with args and kwargs"""
        tst_dt = datetime.utcnow()
        tst_st = Review("1", id="5", created_at=tst_dt.isoformat())
        self.assertEqual(tst_st.id, "5")
        self.assertEqual(tst_st.created_at, tst_dt)

    def test_func_to_dict(self):
        """to_dict method."""
        review_dict = self.review.to_dict()
        self.assertEqual(dict, type(review_dict))
        self.assertEqual(self.review.id, review_dict["id"])
        self.assertEqual("Review", review_dict["__class__"])
        self.assertEqual(self.review.created_at.isoformat(),
                         review_dict["created_at"])
        self.assertEqual(self.review.updated_at.isoformat(),
                         review_dict["updated_at"])
        self.assertEqual(self.review.text, review_dict["text"])
        self.assertEqual(self.review.place_id, review_dict["place_id"])
        self.assertEqual(self.review.user_id, review_dict["user_id"])

    @unittest.skipIf(type(models.storage) is DBStorage,
                     "Test DBStorage")
    def test_func_save_filestorage(self):
        """save method with FileStorage."""
        old_dt = self.review.updated_at
        self.review.save()
        self.assertLess(old_dt, self.review.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("Review." + self.review.id, f.read())

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Test FileStorage")
    def test_func_save_dbstorage(self):
        """save method with DBStorage."""
        old_dt = self.review.updated_at
        self.state.save()
        self.city.save()
        self.user.save()
        self.place.save()
        self.review.save()
        self.assertLess(old_dt, self.review.updated_at)
        db_conn = MySQLdb.connect(user="hbnb_test",
                                  passwd="hbnb_test_func_pwd",
                                  db="hbnb_test_func_db")
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT * \
                          FROM `reviews` \
                          WHERE BINARY text = '{}'".
                          format(self.review.text))
        db_query = db_cursor.fetchall()
        self.assertEqual(1, len(db_query))
        self.assertEqual(self.review.id, db_query[0][0])
        db_cursor.close()


if __name__ == "__main__":
    unittest.main()
