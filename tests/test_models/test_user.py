#!/usr/bin/python3
"""Defines unnittests for models/user.py."""
import os
import pep8
import models
import MySQLdb
import unittest
from datetime import datetime
from models.base_model import Base, BaseModel
from models.user import User
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class TestUser(unittest.TestCase):
    """Unittests for Test the User class."""

    @classmethod
    def setUpClass(cls):
        """User Test setup.

        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates FileStorage, DBStorage and User instances for Test.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.user = User(email="poppy@holberton.com", password="betty98")

        if type(models.storage) is DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """User Test teardown.

        Restore original file.json.
        Delete the FileStorage, DBStorage and User instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.user
        del cls.filestorage
        if type(models.storage) is DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_func_pep8(self):
        """pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/user.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_func_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(User.__doc__)

    def test_func_attributes(self):
        """Check for attributes."""
        us = User(email="a", password="a")
        self.assertEqual(str, type(us.id))
        self.assertEqual(datetime, type(us.created_at))
        self.assertEqual(datetime, type(us.updated_at))
        self.assertTrue(hasattr(us, "__tablename__"))
        self.assertTrue(hasattr(us, "email"))
        self.assertTrue(hasattr(us, "password"))
        self.assertTrue(hasattr(us, "first_name"))
        self.assertTrue(hasattr(us, "last_name"))
        self.assertTrue(hasattr(us, "places"))
        self.assertTrue(hasattr(us, "reviews"))

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Test FileStorage")
    def test_func_email_not_nullable(self):
        """that email attribute is non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(User(password="a"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(User(email="a"))
            self.dbstorage._DBStorage__session.commit()

    def test_func_is_subclass(self):
        """Check User is subclass of BaseModel."""
        self.assertTrue(issubclass(User, BaseModel))

    def test_func_init(self):
        """initialization."""
        self.assertIsInstance(self.user, User)

    def test_func_init_args_kwargs(self):
        """initialization with args and kwargs."""
        tst_dt = datetime.utcnow()
        tst_st = User("1", id="5", created_at=tst_dt.isoformat())
        self.assertEqual(tst_st.id, "5")
        self.assertEqual(tst_st.created_at, tst_dt)

    def test_func_two_models_are_unique(self):
        """that different User instances are unique."""
        usr = User(email="a", password="a")
        self.assertNotEqual(self.user.id, usr.id)
        self.assertLess(self.user.created_at, usr.created_at)
        self.assertLess(self.user.updated_at, usr.updated_at)

    def test_func_to_dict(self):
        """to_dict method."""
        usr_dict = self.user.to_dict()
        self.assertEqual(dict, type(usr_dict))
        self.assertEqual(self.user.id, usr_dict["id"])
        self.assertEqual("User", usr_dict["__class__"])
        self.assertEqual(self.user.created_at.isoformat(),
                         usr_dict["created_at"])
        self.assertEqual(self.user.updated_at.isoformat(),
                         usr_dict["updated_at"])
        self.assertEqual(self.user.email, usr_dict["email"])
        self.assertEqual(self.user.password, usr_dict["password"])

    def test_func_str(self):
        """__str__ representation."""
        tst_st = self.user.__str__()
        self.assertIn("[User] ({})".format(self.user.id), tst_st)
        self.assertIn("'id': '{}'".format(self.user.id), tst_st)
        self.assertIn("'created_at': {}".format(
            repr(self.user.created_at)), tst_st)
        self.assertIn("'updated_at': {}".format(
            repr(self.user.updated_at)), tst_st)
        self.assertIn("'email': '{}'".format(self.user.email), tst_st)
        self.assertIn("'password': '{}'".format(self.user.password), tst_st)

    @unittest.skipIf(type(models.storage) is DBStorage,
                     "Test DBStorage")
    def test_func_save_filestorage(self):
        """save method with FileStorage."""
        old_dt = self.user.updated_at
        self.user.save()
        self.assertLess(old_dt, self.user.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("User." + self.user.id, f.read())

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Test FileStorage")
    def test_func_save_dbstorage(self):
        """save method with DBStorage."""
        old_dt = self.user.updated_at
        self.user.save()
        self.assertLess(old_dt, self.user.updated_at)
        db_conn = MySQLdb.connect(user="hbnb_test",
                                  passwd="hbnb_test_func_pwd",
                                  db="hbnb_test_func_db")
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT * \
                          FROM `users` \
                          WHERE BINARY email = '{}'".
                          format(self.user.email))
        db_query = db_cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.user.id, query[0][0])
        db_cursor.close()


if __name__ == "__main__":
    unittest.main()
