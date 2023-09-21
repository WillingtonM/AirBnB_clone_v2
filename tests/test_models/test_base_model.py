#!/usr/bin/python3
""" """
import os
from models.base_model import BaseModel, Base
import unittest
from datetime import datetime
from uuid import UUID
import json

class test_basemodel(unittest.TestCase):
    """Represents tests for BaseModel """

    def __init__(self, *args, **kwargs):
        """Tests initialisation of model class"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """Performs operations before tests are run"""
        pass

    def tearDown(self):
        """Performs operations after tests are run"""
        try:
            os.remove('file.json')
        except:
            pass

    def test_func_default(self):
        """Tests type of value stored."""
        val = self.value()
        self.assertEqual(type(val), self.value)

    def test_func_kwargs(self):
        """Tests kwargs"""
        val = self.value()
        copy = val.to_dict()
        new_val = BaseModel(**copy)
        self.assertFalse(new is val)

    def test_func_kwargs_int(self):
        """Tests kwargs with an integer"""
        val = self.value()
        copy = val.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new_val = BaseModel(**copy)

    def test_func_save(self):
        """ Testing save """
        val = self.value()
        val.save()
        key = self.name + "." + val.id
        with open('file.json', 'r') as fl:
            js = json.load(fl)
            self.assertEqual(js[key], val.to_dict())

    def test_func_str(self):
        """Tests __str__ function of BaseModel class"""
        val = self.value()
        self.assertEqual(str(val), '[{}] ({}) {}'.format(self.name, val.id,
                         val.__dict__))

    def test_func_todict(self):
        """Tests to_dict function of model class"""
        val = self.value()
        nd = val.to_dict()
        self.assertEqual(val.to_dict(), nd)
        # Tests if it's dictionary
        self.assertIsInstance(self.value().to_dict(), dict)
        self.assertIn('id', self.value().to_dict())
        self.assertIn('created_at', self.value().to_dict())
        self.assertIn('updated_at', self.value().to_dict())
        cls_mdl = self.value()
        cls_mdl.firstname = 'Test'
        cls_mdl.lastname = 'Test'
        self.assertIn('firstname', cls_mdl.to_dict())
        self.assertIn('lastname', cls_mdl.to_dict())
        self.assertIn('firstname', self.value(firstname='Test').to_dict())
        self.assertIn('lastname', self.value(lastname='Test').to_dict())
        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)
        datetime_now = datetime.today()
        cls_mdl = self.value()
        cls_mdl.id = '01234'
        cls_mdl.created_at = cls_mdl.updated_at = datetime_now
        to_dict = {
            'id': '01234',
            '__class__': cls_mdl.__class__.__name__,
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(cls_mdl.to_dict(), to_dict)
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertDictEqual(
                self.value(id='u-b34', age=13).to_dict(),
                {
                    '__class__': cls_mdl.__class__.__name__,
                    'id': 'u-b34',
                    'age': 12
                }
            )
            self.assertDictEqual(
                self.value(id='u-b34', age=None).to_dict(),
                {
                    '__class__': cls_mdl.__class__.__name__,
                    'id': 'u-b34',
                    'age': None
                }
            )
        # Tests to_dict output contradiction
        cls_mdl_d = self.value()
        self.assertIn('__class__', self.value().to_dict())
        self.assertNotIn('__class__', self.value().__dict__)
        self.assertNotEqual(cls_mdl_d.to_dict(), cls_mdl_d.__dict__)
        self.assertNotEqual(
            cls_mdl_d.to_dict()['__class__'],
            cls_mdl_d.__class__
        )
        with self.assertRaises(TypeError):
            self.value().to_dict(None)
        with self.assertRaises(TypeError):
            self.value().to_dict(self.value())
        with self.assertRaises(TypeError):
            self.value().to_dict(45)
        self.assertNotIn('_sa_instance_state', nd)

    def test_func_kwargs_none(self):
        """Tests kwargs that is empty indeed"""
        nd = {None: None}
        with self.assertRaises(TypeError):
            new_val = self.value(**nd)

    def test_func_kwargs_one(self):
        """Tests kwargs with only one key-value pair"""
        nd = {'Name': 'test'}
        with self.assertRaises(KeyError):
            new_val = self.value(**nd)

    def test_func_id(self):
        """Tests type of id"""
        new_val = self.value()
        self.assertEqual(type(new_val.id), str)

    def test_func_created_at(self):
        """Tests type of created_at"""
        new_val = self.value()
        self.assertEqual(type(new_val.created_at), datetime.datetime)

    def test_func_updated_at(self):
        """Tests type of updated_at"""
        new_val = self.value()
        self.assertEqual(type(new_val.updated_at), datetime.datetime)
        n = new_val.to_dict()
        new_val = BaseModel(**n)
        self.assertFalse(new_val.created_at == new_val.updated_at)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_func_delete(self):
        """Tests delete function of BaseModel class."""
        from models import storage
        val = self.value()
        val.save()
        self.assertTrue(val in storage.all().values())
        val.delete()
        self.assertFalse(val in storage.all().values())
