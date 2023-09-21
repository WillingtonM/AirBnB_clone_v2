#!/usr/bin/python3
""" """
import os
from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(test_basemodel):
    """Represents tests for State model"""

    def __init__(self, *args, **kwargs):
        """Initialises test class"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_func_name3(self):
        """Tests type of name"""
        new_val = self.value()
        self.assertEqual(type(new_val.name), 
                         str if os.getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
                         )
