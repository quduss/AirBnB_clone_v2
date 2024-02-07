#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
import models
import shlex
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", cascade='all, delete, delete-orphan',
                              backref="state")

    else:
        @property
        def cities(self):
            objects = models.storage.all()
            all_cities = []
            my_cities = []
            for key in objects:
                obj_key = key.replace('.', ' ')
                obj_key = shlex.split(obj_key)
                if (obj_key[0] == 'City'):
                    all_cities.append(objects[key])
            for city in all_cities:
                if (city.state_id == self.id):
                    my_cities.append(city)
            return (my_cities)
