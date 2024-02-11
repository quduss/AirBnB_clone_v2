#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv
import models
import shlex


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                               backref="place")

        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            """ Returns my list of reviews """
            all_objects = models.storage.all()
            all_reviews = []
            my_reviews = []
            for key in all_objects:
                key_ = key.replace('.', ' ')
                key_ = shlex.split(key_)
                if (key_[0] == 'Review'):
                    all_reviews.append(all_objects[key])
            for obj in all_reviews:
                if (obj.place_id == self.id):
                    my_reviews.append(obj)
            return (my_reviews)

        @property
        def amenities(self):
            """getter attribute that returns list of amenities
            for Place object"""
            my_amenities = []
            all_objects = models.storage.all()
            for id_ in self.amenity_ids:
                key = "Amenity." + id_
                my_amenities.append(all_objects[key])
            return my_amenities

        @amenities.setter
        def amenities(self, id_):
            """Appends an amenity.id to amenity_ids"""
            key = "Amenity." + id_
            all_objects = models.storage.all()
            if key in all_objects:
                self.amenity_ids.append(id_)
