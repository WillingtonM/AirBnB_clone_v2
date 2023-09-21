#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:43:09 2020
@author: meco
"""
import io
import sys
import pep8
import inspect
import unittest
from datetime import datetime
from contextlib import redirect_stdout
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models import storage


class TestFileStorage(unittest.TestCase):
    """
    class for testing FileStorage class' methods
    """
    tmp_file = ""

    @classmethod
    def set_up_class(cls):
        """
        Set up class method for doc tests
        """
        cls.setup = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_func_pep8_conformance_test_FileStorage(self):
        """
        Function that tests test_file_storage.py file conform to PEP8
        """
        pep8_stl = pep8.StyleGuide(quiet=True)
        pep8_res = pep8_stl.check_files(['tests/test_models/\
                                        test_file_storage.py'])
        self.assertEqual(pep8_res.total_errors, 1,
                         "Found code style errors (and warnings).")

    def test_func_pep8_conformance_FileStorage(self):
        """
        Function that tests the file_storage.py file conform to PEP8
        """
        pep8_stl = pep8.StyleGuide(quiet=True)
        pep8_res = pep8_stl.check_files(['models/file_storage.py'])
        self.assertEqual(pep8_res.total_errors, 1,
                         "Found code style errors (and warnings).")
    def test_func_class_docstring(self):
        """
        Function that tests if class docstring documentation exist
        """
        self.assertTrue(len(FileStorage.__doc__) >= 1)

    def test_func_docstrings(self):
        """
        Function that tests if methods docstring documntation exist
        """
        for fnc in self.setup:
            self.assertTrue(len(fnc[1].__doc__) >= 1)

    def test_func_module_docstring(self):
        """
        Function that tests if module docstring documentation exist
        """
        self.assertTrue(len(FileStorage.__doc__) >= 1)

    @staticmethod
    def move_file_func(src, dest):
        with open(src, 'r', encoding='utf-8') as my_file:
            with open(dest, 'w', encoding='utf-8') as tmp_file:
                tmp_file.write(my_file.read())
        os.remove(src)

    def set_up(self):
        self.tmp_file = '/temp_store.json'
        self.tmp_objs = [BaseModel(), BaseModel(), BaseModel()]
        for obj in self.tmp_objs:
            storage.new(obj)
        storage.save()

    def tear_down(self):
        """
        Initialised object
        """
        del self.tmp_objs

    def test_func_type(self):
        """
        type checks for FileStorage
        """
        self.assertIsInstance(storage, FileStorage)
        self.assertEqual(type(storage), FileStorage)

    def test_func_save(self):
        """
        Function that tests save functionality for FileStorage
        """
        with open('file.json', 'r', encoding='utf-8') as my_file:
            dmp = my_file.read()
        self.assertNotEqual(len(dmp), 0)
        temp_eval = eval(dmp)
        key_1 = self.tmp_objs[0].__class__.__name__ + '.'
        key_1 += str(self.tmp_objs[0].id)
        self.assertNotEqual(len(temp_eval[key_1]), 0)
        key_2 = 'State.412409120491902491209491024'
        try:
            self.assertRaises(temp_eval[key_2], KeyError)
        except:
            pass

    def test_func_reload(self):
        """
        Function that tests reload functionality for FileStorage
        """
        storage.reload()
        obj_sto = storage.all()
        key_1 = self.tmp_objs[1].__class__.__name__ + '.'
        key_1 += str(self.tmp_objs[1].id)
        self.assertNotEqual(obj_sto[key_1], None)
        self.assertEqual(obj_sto[key_1].id, self.tmp_objs[1].id)
        key_2 = 'State.412409120491902491209491024'
        try:
            self.assertRaises(obj_sto[key_2], KeyError)
        except:
            pass

    def test_func_delete_basic(self):
        """
        Function that tests delete basic functionality for FileStorage
        """
        obj_sto = storage.all()
        key_2 = self.tmp_objs[2].__class__.__name__ + '.'
        key_2 += str(self.tmp_objs[2].id)
        try:
            self.assertRaises(obj_sto[key_2], KeyError)
        except:
            pass

    def test_func_new_basic(self):
        """
        Function that tests new basic functionality for FileStorage
        """
        obj = BaseModel()
        storage.new(obj)
        obj_sto = storage.all()
        key_1 = obj.__class__.__name__ + '.' + str(obj.id)
        self.assertEqual(obj_sto[key_1] is obj, True)

    def test_func_new_badinput(self):
        """
        Function that tests new bad input functionality  FileStorage
        """
        try:
            self.assertRaises(storage.new('jwljfef'), TypeError)
            self.assertRaises(storage.new(None), TypeError)
        except:
            pass
