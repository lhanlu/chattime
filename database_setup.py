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

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

class Contact(Base):

    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'belong_to': self.user.name,
        }


class Message(Base):

    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    time = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    contact = relationship(Contact)
    
    @property
    def serialize(self):
        return{
            'id': self.id,
            'content': self.content,
            'time': self.time,
            'sender': self.user.name,
            'receiver': self.contact.name,
        }



### insert at end of file ###


engine = create_engine('sqlite:///chattime.db')

Base.metadata.create_all(engine)
