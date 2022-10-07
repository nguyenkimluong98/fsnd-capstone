import os
from sqlalchemy import ForeignKey, Column, String, Integer, \
  Date, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
import os
from flask_migrate import Migrate

database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  migrate = Migrate(app, db)

class Book(db.Model):

  __tablename__ = 'books'

  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String)
  description = Column(String)
  release_date = Column(Date)
  author_id = Column(Integer, ForeignKey("authors.id"))
  author = relationship("Author", back_populates="books")

  def __init__(self, title, description, release_date, author_id):
      self.title = title
      self.description = description
      self.release_date = release_date
      self.author_id = author_id

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def update(self):
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def short(self):
    return {
          'id': self.id,
          'title': self.title,
          'author': self.author.name
      }

  def long(self):
      return {
          'id': self.id,
          'title': self.title,
          'description': self.description,
          'release_date': self.release_date,
          'author': self.author.name
      }

class Author(db.Model):

  __tablename__ = 'authors'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String)
  full_name = Column(String)
  dob = Column(Date)
  books = relationship('Book', back_populates="author")

  def __init__(self, name, full_name, dob):
      self.name = name
      self.full_name = full_name
      self.dob = dob

  def insert(self):
      db.session.add(self)
      db.session.commit()

  def update(self):
      db.session.commit()

  def delete(self):
      db.session.delete(self)
      db.session.commit()

  def short(self):
    return {
          'id': self.id,
          'name': self.name
      }

  def long(self):
    return {
        'id': self.id,
        'name': self.name,
        'full_name': self.full_name,
        'dob': self.dob,
        'number_of_books': len(self.books)
    }