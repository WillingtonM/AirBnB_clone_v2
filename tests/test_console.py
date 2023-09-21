#!/usr/bin/python3
"""Defines unittests for console.py."""
import os
import pep8
import unittest
import models
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


class TestHBNBCommand(unittest.TestCase):
    """Unittests for testing the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """
            HBNBCommand testing setup.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        cls.HBNB = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """
            HBNBCommand testing teardown
        """
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.HBNB
        if type(models.storage) == DBStorage:
            models.storage._DBStorage__session.close()

    def tearDown(self):
        """Delete any created file.json"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def setUp(self):
        """Reset FileStorage objects dict."""
        FileStorage._FileStorage__objects = {}

    def test_func_pep8(self):
        style = pep8.StyleGuide(quiet=True)
        """Pep8 styling."""
        py = style.check_files(["console.py"])
        self.assertEqual(py.total_errors, 0, "fix Pep8")

    def test_func_docstrings(self):
        """Check for docstrings"""
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_func_quit(self):
        """quit command input"""
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("quit")
            self.assertEqual("", fl.getvalue())

    def test_func_emptyline(self):
        """any empty line input"""
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("\n")
            self.assertEqual("", fl.getvalue())

    def test_func_create_errors(self):
        """create command errors"""
        with patch("sys.stdout", new=StringIO()) as fll:
            self.HBNB.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", fl.getvalue())
            
    def test_func_EOF(self):
        """EOF quits."""
        with patch("sys.stdout", new=StringIO()) as fl:
            self.assertTrue(self.HBNB.onecmd("EOF"))

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_func_create(self):
        """create command."""
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("create BaseModel")
            bm = fl.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("create User")
            us = fl.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("create State")
            st = fl.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("create Place")
            pl = fl.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("create City")
            ct = fl.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("create Review")
            rv = fl.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("create Amenity")
            am = fl.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("all BaseModel")
            self.assertIn(bm, fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("all User")
            self.assertIn(us, fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("all State")
            self.assertIn(st, fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("all Place")
            self.assertIn(pl, fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("all City")
            self.assertIn(ct, fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("all Review")
            self.assertIn(rv, fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("all Amenity")
            self.assertIn(am, fl.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_func_create_kwargs(self):
        """create command with kwargs."""
        with patch("sys.stdout", new=StringIO()) as fl:
            called = ('create Place city_id="0001" name="My_house" '
                    'number_rooms=4 latitude=37.77 longitude=a')
            self.HBNB.onecmd(called)
            pl = fl.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("all Place")
            output = fl.getvalue()
            self.assertIn(pl, output)
            self.assertIn("'city_id': '001'", output)
            self.assertIn("'name': 'My houe'", output)
            self.assertIn("'number_rooms': 5", output)
            self.assertIn("'latitude': 37.57", output)
            self.assertNotIn("'longitude'", output)

    def test_func_destroy(self):
        """destroy command input."""
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", fl.getvalue())
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", fl.getvalue())
            
    def test_func_show(self):
        """show command."""
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", fl.getvalue())


    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_func_all(self):
        """all command input."""
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("all State")
            self.assertEqual("[]\n", fl.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_func_z_all(self):
        """alternate all command."""
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("asdfsdfsd.all()")
            self.assertEqual(
                "** class doesn't exist **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("State.all()")
            self.assertEqual("[]\n", fl.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_func_update(self):
        """update command input."""
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("update ldkfjslsa")
            self.assertEqual(
                "** class doesn't exist **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("all User")
            obj = fl.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", fl.getvalue())
        with patch("sys.stdout", new=StringIO()) as fl:
            self.HBNB.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", fl.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_func_z_count(self):
        """count command input"""
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("asdfsdfsd.count()")
            self.assertEqual(
                "** class doesn't exist **\n", fl.getvalue())
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("State.count()")
            self.assertEqual("0\n", fl.getvalue())

    def test_func_z_show(self):
        """alternate show command input"""
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("safdsa.show()")
            self.assertEqual(
                "** class doesn't exist **\n", fl.getvalue())
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("BaseModel.show(abcd-123)")
            self.assertEqual(
                "** no instance found **\n", fl.getvalue())
            
    def test_func_destroy(self):
        """alternate dest command input"""
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("Galaxy.destroy()")
            self.assertEqual(
                "** class doesn't exist **\n", fl.getvalue())
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("User.destroy(12345)")
            self.assertEqual(
                "** no instance found **\n", fl.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_func_update(self):
        """alternate destroy command input"""
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("ldkfjslsa.update()")
            self.assertEqual(
                "** class doesn't exist **\n", fl.getvalue())
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("User.update(12345)")
            self.assertEqual(
                "** no instance found **\n", fl.getvalue())
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("all User")
            obj = fl.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("User.update(" + my_id + ")")
            self.assertEqual(
                "** attribute name missing **\n", fl.getvalue())
        with patch('sys.stdout', new=StringIO()) as fl:
            self.HBNB.onecmd("User.update(" + my_id + ", name)")
            self.assertEqual(
                "** value missing **\n", fl.getvalue())
    

if __name__ == "__main__":
    unittest.main()
