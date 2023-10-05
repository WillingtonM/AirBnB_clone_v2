#!/usr/bin/python3
""" """
import os
from tests.test_models.test_base_model import test_basemodel
from models.place import Place


class test_Place(test_basemodel):
    """Represents tests for Place model"""

    def __init__(self, *args, **kwargs):
        """Initialises test class"""
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_func_city_id(self):
        """Tests the type of city_id"""
        new_val = self.value()
        self.assertEqual(type(new_val.city_id),
                         str if os.getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_func_user_id(self):
        """ """
        new_val = self.value()
        self.assertEqual(type(new_val.user_id),
                         str if os.getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_func_name(self):
        """ """
        new_val = self.value()
        self.assertEqual(type(new_val.name),
                         str if os.getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_func_description(self):
        """ """
        new_val = self.value()
        self.assertEqual(type(new_val.description),
                         str if os.getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_func_number_rooms(self):
        """ """
        new_val = self.value()
        self.assertEqual(type(new_val.number_rooms),
                         int if os.getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_func_number_bathrooms(self):
        """ """
        new_val = self.value()
        self.assertEqual(type(new_val.number_bathrooms),
                         int if os.getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_func_max_guest(self):
        """ """
        new_val = self.value()
        self.assertEqual(type(new_val.max_guest),
                         int if os.getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_func_price_by_night(self):
        """ """
        new_val = self.value()
        self.assertEqual(type(new_val.price_by_night),
                         int if os.getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_func_latitude(self):
        """ """
        new_val = self.value()
        self.assertEqual(type(new_val.latitude),
                         float if os.getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_func_longitude(self):
        """ """
        new_val = self.value()
        self.assertEqual(type(new_val.latitude),
                         float if os.getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_func_amenity_ids(self):
        """ """
        new_val = self.value()
        self.assertEqual(type(new_val.amenity_ids), list)
