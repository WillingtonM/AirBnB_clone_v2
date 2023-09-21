#!/usr/bin/python3
""" """
import os
from tests.test_models.test_base_model import test_basemodel
from models.city import City


class test_City(test_basemodel):
    """Tests for the City model"""

    def __init__(self, *args, **kwargs):
        """Initialises test class"""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_func_state_id(self):
        """Tests type of state_id"""
        new_val = self.value()
        self.assertEqual(type(new_val.state_id), 
                         str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
                         )

    def test_func_name(self):
        """Tests type of name. """
        new_val = self.value()
        self.assertEqual(type(new_val.name), 
                         str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
                         )
