#!/usr/bin/python3
"""Defines the DBStorage class backed by a MySQL database via SQLAlchemy."""
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Interacts with a MySQL database using the SQLAlchemy ORM.

    Private instance attributes:
        __engine: the SQLAlchemy engine bound to the configured database.
        __session: the current SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Create the engine and drop all tables in test mode."""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db),
            pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of cls (or every type) from the database.

        Return a dictionary keyed by ``<class name>.id``.
        """
        classes = [User, State, City, Amenity, Place, Review]
        if cls is not None:
            if isinstance(cls, str):
                classes = [c for c in classes if c.__name__ == cls]
            else:
                classes = [cls]
        result = {}
        for klass in classes:
            for obj in self.__session.query(klass).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                result[key] = obj
        return result

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session, if not None."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and a fresh thread-safe session."""
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)

    def close(self):
        """Close the current session by removing it from the registry."""
        self.__session.remove()
