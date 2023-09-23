#!/usr/bin/python3
"""
Contains the TestCityDocs classes
"""
import os
import pep8
import unittest
import MySQLdb
import models
from datetime import datetime
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError


class TestCity(unittest.TestCase):
    """Unnittest to check the City class"""

    def test_func_docstrings(self):
        """Check docstrings."""
        self.assertIsNotNone(City.__doc__)

    def test_func_pep8(self):
        """Test pep8 styling."""
        tst_style = pep8.StyleGuide(quiet=True)
        tst_p = tst_style.check_files(["models/city.py"])
        self.assertEqual(tst_p.total_errors, 0, "fix pep8")

    def test_func_attributes(self):
        """Check attributes."""
        cty = City()
        self.assertEqual(str, type(cty.id))
        self.assertEqual(datetime, type(cty.created_at))
        self.assertEqual(datetime, type(cty.updated_at))
        self.assertTrue(hasattr(cty, "__tablename__"))
        self.assertTrue(hasattr(cty, "name"))
        self.assertTrue(hasattr(cty, "state_id"))

    @classmethod
    def setUpClass(cls):
        """ City Test setup"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)

        if type(models.storage) is DBStorage:
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """ City Test teardown """
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
        del cls.filestorage
        if type(models.storage) is DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Test FileStorage")
    def test_func_nullable_attributes(self):
        """Check relevant DBStorage attributes are non-nullable."""
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(City(
                state_id=self.state.id))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            self.dbstorage._DBStorage__session.add(City(name="San Jose"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Test FileStorage")
    def test_func_state_relationship_deletes(self):
        """Test delete cascade in City-State relationship."""
        stat = State(name="Georgia")
        self.dbstorage._DBStorage__session.add(stat)
        self.dbstorage._DBStorage__session.commit()
        cty = City(name="Atlanta", state_id=stat.id)
        self.dbstorage._DBStorage__session.add(cty)
        self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.delete(stat)
        self.dbstorage._DBStorage__session.commit()
        db_conn = MySQLdb.connect(user="hbnb_test",
                                  passwd="hbnb_test_func_pwd",
                                  db="hbnb_test_func_db")
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT * FROM cities WHERE BINARY name = 'Atlanta'")
        query = db_cursor.fetchall()
        db_cursor.close()
        self.assertEqual(0, len(db_cursor))

    def test_func_init(self):
        """Test initialization."""
        self.assertIsInstance(self.city, City)

    def test_func_is_subclass(self):
        """Check City is subclass of BaseModel"""
        self.assertTrue(issubclass(City, BaseModel))

    def test_func_to_dict(self):
        """Test to_dict method."""
        city_dict = self.city.to_dict()
        self.assertEqual(dict, type(city_dict))
        self.assertEqual(self.city.id, city_dict["id"])
        self.assertEqual("City", city_dict["__class__"])
        self.assertEqual(self.city.created_at.isoformat(),
                         city_dict["created_at"])
        self.assertEqual(self.city.updated_at.isoformat(),
                         city_dict["updated_at"])
        self.assertEqual(self.city.name, city_dict["name"])
        self.assertEqual(self.city.state_id, city_dict["state_id"])

    def test_func_two_models_are_unique(self):
        """Test different City instances are unique"""
        cty = City()
        self.assertNotEqual(self.city.id, cty.id)
        self.assertLess(self.city.created_at, cty.created_at)
        self.assertLess(self.city.updated_at, cty.updated_at)

    def test_func_str(self):
        """Test __str__ representation"""
        st = self.city.__str__()
        self.assertIn("[City] ({})".format(self.city.id), st)
        self.assertIn("'id': '{}'".format(self.city.id), st)
        self.assertIn("'created_at': {}".format(
            repr(self.city.created_at)), st)
        self.assertIn("'updated_at': {}".format(
            repr(self.city.updated_at)), st)
        self.assertIn("'name': '{}'".format(self.city.name), st)
        self.assertIn("'state_id': '{}'".format(self.city.state_id), st)

    def test_func_init_args_kwargs(self):
        """Test initialization with args & kwargs."""
        dtm = datetime.utcnow()
        cty = City("1", id="5", created_at=dtm.isoformat())
        self.assertEqual(cty.id, "5")
        self.assertEqual(cty.created_at, dtm)

    @unittest.skipIf(type(models.storage) is DBStorage,
                     "Test DBStorage")
    def test_func_save_filestorage(self):
        """Test save method with FileStorage."""
        old_dt = self.city.updated_at
        self.city.save()
        self.assertLess(old_dt, self.city.updated_at)
        with open("file.json", "r") as fl:
            self.assertIn("City." + self.city.id, fl.read())

    @unittest.skipIf(type(models.storage) is FileStorage,
                     "Test FileStorage")
    def test_func_save_dbstorage(self):
        """Test save method with DBStorage."""
        old_dt = self.city.updated_at
        self.state.save()
        self.city.save()
        self.assertLess(old_dt, self.city.updated_at)
        db_conn = MySQLdb.connect(user="hbnb_test",
                                  passwd="hbnb_test_func_pwd",
                                  db="hbnb_test_func_db")
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT * \
                          FROM `cities` \
                          WHERE BINARY name = '{}'".
                          format(self.city.name))
        db_query = db_cursor.fetchall()
        self.assertEqual(1, len(db_query))
        self.assertEqual(self.city.id, db_query[0][0])
        db_cursor.close()


if __name__ == "__main__":
    unittest.main()
