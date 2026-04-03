from sqlalchemy import Column, Integer, String
from database import Base

class Animal(Base):
    __tablename__ = 'animals'
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String)
    age = Column(Integer)
    gender = Column(String)
    status = Column(String)
    contact = Column(String)
    description = Column(String)

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer)
    lat = Column(String)
    lon = Column(String)

class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True, index=True)
    lost_id = Column(Integer)
    found_id = Column(Integer)
    con_score = Column(String)

