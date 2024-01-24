from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class twoWords(Base):
    __tablename__ = 'twoWords'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)

class twoWordsName(Base):
    __tablename__ = 'twoWordsName'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)

class threeWords(Base):
    __tablename__ = 'threeWords'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)

class threeWordsName(Base):
    __tablename__ = 'threeWordsName'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)