#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all cls objects present in
        __objects if cls is given else return all objects"""
        classes = [BaseModel, User, Place, State, City, Amenity, Review]
        if cls in classes:
            all_objects = FileStorage.__objects
            cls_objects = {}
            for key in all_objects.keys():
                if type(all_objects[key]) is cls:
                    cls_objects[key] = all_objects[key]
            return cls_objects
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj if it's inside __objects"""
        classes = [BaseModel, User, Place, State, City, Amenity, Review]
        cls = type(obj)
        if cls in classes:
            key = f"{cls.__name__}.{obj.id}"
            objects = FileStorage.__objects
            try:
                del objects[key]
            except KeyError:
                pass
        else:
            pass
