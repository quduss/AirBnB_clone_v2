from models.base_model import Base
from sqlalchemy import create_engine
from os import getenv
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialising db storage"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary of all cls objects if cls is given
        otherwise all objects"""
        dict_ = {}
        if cls:
            cls_objects = self.__session.query(cls)
            for obj in cls_objects:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                dict_[key] = obj
        else:
            classes = [City, State, User]
            for class_ in classes:
                cls_objects = self.__session.query(class_)
                for obj in cls_objects:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    dict_[key] = obj
        return (dict_)

    def new(self, obj):
        """add obj to the current database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj if not none from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database
        create the current database session(self.__session)"""
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()
