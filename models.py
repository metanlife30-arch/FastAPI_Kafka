from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Аuthor(Base):
    __tablename__ = 'Аuthor'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    
class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    password = Column(String,index=True)

class Post(Base):
    __tablename__ = 'Post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)
    author_id = Column(Integer, ForeignKey('Аuthor.id'))
    author = relationship('Аuthor')

