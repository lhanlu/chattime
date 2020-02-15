import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)



class Contact(Base):

    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)



class Message(Base):

    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    time = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    contact = relationship(Contact)



### insert at end of file ###


engine = create_engine('sqlite:///chattime.db')

Base.metadata.create_all(engine)
