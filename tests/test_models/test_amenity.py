#!/usr/bin/python3
"""Defines unnittests for models/amenity.py."""
import os
import pep8
import MySQLdb
import unittest
import models
from models.base_model import Base, BaseModel
from datetime import datetime
from models.amenity import Amenity
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError


class TestAmenity(unittest.TestCase):
    """Unittests for Test Amenity class"""

    @classmethod
    def setUpClass(cls):
        """
            Amenity Test setup.

            Temporarily renames any existing file.json.
            Resets FileStorage objects dictionary.
            Creates FileStorage, DBStorage and Amenity instances for Test.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.amenity = Amenity(name="The Andrew Lindburg treatment")

        if type(models.storage) is DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """
            Amenity Test teardown.
            Restore original file.json.
            Delete FileStorage, DBStorage and Amenity test instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.amenity
        del cls.filestorage
        if type(models.storage) is DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_func_pep8_conformance_amenity(self):
        """Test models/amenity.py conforms to PEP8"""
        pep = pep8.StyleGuide(quiet=True)
        res = pep.check_files(['models/amenity.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_func_pep8_conformance_test_func_amenity(self):
        """Test tests/test_func_models/test_func_amenity.py conforms to PEP8"""
        pep = pep8.StyleGuide(quiet=True)
        res = pep.check_files(['tests/test_func_models/test_func_amenity.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_func_docstrings(self):
        """Check docstrings."""
        self.assertIsNotNone(Amenity.__doc__)

    def test_func_attributes(self):
        """Check attributes."""
        usr = Amenity(email="a", password="a")
        self.assertEqual(str, type(usr.id))
        self.assertEqual(datetime, type(usr.created_at))
        self.assertEqual(datetime, type(usr.updated_at))
        self.assertTrue(hasattr(usr, "__tablename__"))
        self.assertTrue(hasattr(usr, "name"))
        self.assertTrue(hasattr(usr, "place_amenities"))

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Test FileStorage")
    def test_func_email_not_nullable(self):
        """Test email attribute is non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Amenity(password="a"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(Amenity(email="a"))
            self.dbstorage._DBStorage__session.commit()

    def test_func_is_subclass(self):
        """Check that Amenity is a subclass of BaseModel."""
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_func_init(self):
        """Test initialization."""
        self.assertIsInstance(self.amenity, Amenity)

    def test_func_two_models_are_unique(self):
        """Test different Amenity instances are unique."""
        usr = Amenity(email="a", password="a")
        self.assertNotEqual(self.amenity.id, usr.id)
        self.assertLess(self.amenity.created_at, usr.created_at)
        self.assertLess(self.amenity.updated_at, usr.updated_at)

    def test_func_init_args_kwargs(self):
        """Test initialization with args & kwargs."""
        am_dt = datetime.utcnow()
        am_st = Amenity("1", id="5", created_at=am_dt.isoformat())
        self.assertEqual(am_st.id, "5")
        self.assertEqual(am_st.created_at, am_dt)

    def test_func_str(self):
        """Test __str__ representation."""
        st = self.amenity.__str__()
        self.assertIn("[Amenity] ({})".format(self.amenity.id), st)
        self.assertIn("'id': '{}'".format(self.amenity.id), st)
        self.assertIn("'created_at': {}".format(
            repr(self.amenity.created_at)), st)
        self.assertIn("'updated_at': {}".format(
            repr(self.amenity.updated_at)), st)
        self.assertIn("'name': '{}'".format(self.amenity.name), st)

    @unittest.skipIf(type(models.storage) is DBStorage,
                     "Test DBStorage")
    def test_func_save_filestorage(self):
        """Test save method with FileStorage."""
        old_dt = self.amenity.updated_at
        self.amenity.save()
        self.assertLess(old_dt, self.amenity.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("Amenity." + self.amenity.id, f.read())

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Test FileStorage")
    def test_func_save_dbstorage(self):
        """Test save method with DBStorage."""
        old_dt = self.amenity.updated_at
        self.amenity.save()
        self.assertLess(old_dt, self.amenity.updated_at)
        db_conn = MySQLdb.connect(user="hbnb_test",
                                  passwd="hbnb_test_func_pwd",
                                  db="hbnb_test_func_db")
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT * \
                          FROM `amenities` \
                          WHERE BINARY name = '{}'".
                          format(self.amenity.name))
        sql_query = db_cursor.fetchall()
        self.assertEqual(1, len(sql_query))
        self.assertEqual(self.amenity.id, sql_query[0][0])
        db_cursor.close()

    def test_func_to_dict(self):
        """Test to_dict method."""
        amnt_dict = self.amenity.to_dict()
        self.assertEqual(dict, type(amnt_dict))
        self.assertEqual(self.amenity.id, amnt_dict["id"])
        self.assertEqual("Amenity", amnt_dict["__class__"])
        self.assertEqual(self.amenity.created_at.isoformat(),
                         amnt_dict["created_at"])
        self.assertEqual(self.amenity.updated_at.isoformat(),
                         amnt_dict["updated_at"])
        self.assertEqual(self.amenity.name, amnt_dict["name"])


if __name__ == "__main__":
    unittest.main()
