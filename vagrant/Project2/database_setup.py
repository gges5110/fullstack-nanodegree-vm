# Configuration
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
# End of Configuration

# Class
class Restaurant(Base):
    # Table
    __tablename__ = 'restaurant'

    # Mapper
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

# Class
class MenuItem(Base):
    # Table
    __tablename__ = 'menu_item'

    # Mapper
    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))

    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course
        }

# Configuration
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
# End of Configuration
