#!/usr/bin/python3
""" """
import os
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity


class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """Represents tests for Amenity model"""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_func_name2(self):
        """Tests type of name"""
        new = self.value()
        self.assertEqual(type(new.name), str)
