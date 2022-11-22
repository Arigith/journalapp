from sqlalchemy import Column, Integer, String, ForeignKey, Date
from database import Base
from sqlalchemy.orm import relationship
from datetime import date

class Journal(Base):
    __tablename__='Journals'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body=Column(String)
    date_created=Column(Date, default=date.today())
    user_id=Column(Integer,ForeignKey('Users.id'))
    creator=relationship('User',back_populates='journals')

class User(Base):
    __tablename__='Users'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String)
    password=Column(String)
    journals=relationship('Journal',back_populates='creator')