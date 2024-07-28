#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity


if getenv("HBNB_TYPE_STORAGE") == "db":
    from .engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from .engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
