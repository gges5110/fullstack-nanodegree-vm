# Configuration
import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
# End of Configuration

# Class
class User(Base):
    # Table
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'picture' : self.picture
        }

# Class
class Catalog(Base):
    # Table
    __tablename__ = 'catalog'

    # Mapper
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id
        }

# Class
class Item(Base):
    # Table
    __tablename__ = 'item'

    # Mapper
    title = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(Integer, nullable = False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    picture = Column(String(250))

    catalog_id = Column(Integer,ForeignKey('catalog.id'))
    catalog = relationship(Catalog)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'title' : self.title,
            'description' : self.description,
            'price' : self.price,
            'created_date' : self.created_date.isoformat(),
            'id' : self.id,
            'user_id' : self.user_id
        }

# Configuration
engine = create_engine('sqlite:///catalogwithusers.db')
Base.metadata.create_all(engine)
# End of Configuration
