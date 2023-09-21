#!/usr/bin/python3
""" """
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
        new = self.value()
        self.assertEqual(type(new.city_id), str)

    def test_func_user_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    def test_func_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_func_description(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.description), str)

    def test_func_number_rooms(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.number_rooms), int)

    def test_func_number_bathrooms(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.number_bathrooms), int)

    def test_func_max_guest(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.max_guest), int)

    def test_func_price_by_night(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.price_by_night), int)

    def test_func_latitude(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), float)

    def test_func_longitude(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), float)

    def test_func_amenity_ids(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list)
