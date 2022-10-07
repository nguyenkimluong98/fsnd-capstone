
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Book, Author


class BookStoreTest(unittest.TestCase):
    """This class represents the bookstore test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_books(self):
      res = self.client().get('/books')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data["success"], True)
      self.assertTrue(len(data["books"]))

    def test_error_get_all_books(self):
      res = self.client().get('/book')
      data = json.loads(res.data)
      self.assertNotEqual(res.status_code, 200)
      self.assertNotEqual(data["success"], True)

    def test_get_all_authors(self):
      res = self.client().get('/authors')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data["success"], True)
      self.assertTrue(len(data["authors"]))

    def test_error_get_all_authors(self):
      res = self.client().get('/author')
      data = json.loads(res.data)
      self.assertNotEqual(res.status_code, 200)
      self.assertNotEqual(data["success"], True)

    def test_get_all_books_of_author(self):
      res = self.client().get('/books/author/1')
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data["success"], True)
      self.assertTrue(len(data["books"]))

    def test_error_get_all_books_of_author(self):
      res = self.client().get('/books/author/test')
      data = json.loads(res.data)
      self.assertNotEqual(res.status_code, 200)
      self.assertNotEqual(data["success"], True)

    def test_create_book(self):
      res = self.client().post("/books", json={
        "title": "test_book",
        "description": "test_desc",
        "release_date": "2022/03/09",
        "author_id": 2
      })
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data["success"], True)
      self.assertTrue(len(data["books"]))

      book_id = data['books'][0].get('id')
      self.client().delete("/books/{id}".format(id=book_id))

    def test_error_create_book(self):
      res = self.client().post("/books", json={
        "title": "",
      })
      data = json.loads(res.data)
      self.assertNotEqual(res.status_code, 200)
      self.assertNotEqual(data["success"], True)

    def test_create_author(self):
      res = self.client().post("/authors", json={
        "name": "test_author",
        "full_name": "test_desc",
        "dob": "2022/03/09"
      })

      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data["success"], True)
      self.assertTrue(len(data["authors"]))

      author_id = data['authors'][0].get('id')
      self.client().delete("/authors/{id}".format(id=author_id))

    def test_error_create_author(self):
      res = self.client().post("/authors", json={
        "name": "",
      })
      data = json.loads(res.data)
      self.assertNotEqual(res.status_code, 200)
      self.assertNotEqual(data["success"], True)

    def test_edit_book(self):
      res = self.client().post("/books", json={
        "title": "test_book",
        "description": "test_desc",
        "release_date": "2022/03/09",
        "author_id": 2
      })
      data = json.loads(res.data)

      book_id = data['books'][0].get('id')

      res = self.client().patch("/books/{id}".format(id=book_id), json={
        "title": "edited_title"
      })

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data["success"], True)
      self.assertTrue(len(data["books"]))
      self.assertTrue(data['books'][0].get('title'), "edited_title")

      self.client().delete("/books/{id}".format(id=book_id))

    def test_error_edit_book(self):
      res = self.client().patch("/books/error_id", json={
        "title": "edited_title"
      })
      data = json.loads(res.data)

      self.assertNotEqual(res.status_code, 200)
      self.assertNotEqual(data["success"], True)

    def test_edit_author(self):
      res = self.client().post("/authors", json={
        "name": "test_author",
        "full_name": "test_desc",
        "dob": "2022/03/09"
      })
      data = json.loads(res.data)

      author_id = data['authors'][0].get('id')

      res = self.client().patch("/authors/{id}".format(id=author_id), json={
        "name": "edited_name"
      })

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data["success"], True)
      self.assertTrue(len(data["authors"]))
      self.assertTrue(data['authors'][0].get('name'), "edited_name")

      self.client().delete("/authors/{id}".format(id=author_id))

    def test_error_edit_author(self):
      res = self.client().patch("/authors/error_id", json={
        "name": "edited_name"
      })
      data = json.loads(res.data)

      self.assertNotEqual(res.status_code, 200)
      self.assertNotEqual(data["success"], True)

    def test_delete_author(self):
      res = self.client().post("/authors", json={
        "name": "test_author",
        "full_name": "test_desc",
        "dob": "2022/03/09"
      })
      data = json.loads(res.data)
      author_id = data['authors'][0].get('id')

      res = self.client().delete("/authors/{id}".format(id=author_id))

      self.assertEqual(res.status_code, 200)

    def test_error_delete_author(self):
      res = self.client().delete("/authors/error_id")
      data = json.loads(res.data)

      self.assertNotEqual(res.status_code, 200)
      self.assertNotEqual(data["success"], True)

    def test_delete_book(self):
      res = self.client().post("/books", json={
        "title": "test12",
        "description": "1",
        "release_date": "2022/03/09",
        "author_id": 2
      })
      data = json.loads(res.data)
      book_id = data['books'][0].get('id')

      res = self.client().delete("/books/{id}".format(id=book_id))

      self.assertEqual(res.status_code, 200)

    def test_error_delete_book(self):
      res = self.client().delete("/books/error_id")
      data = json.loads(res.data)

      self.assertNotEqual(res.status_code, 200)
      self.assertNotEqual(data["success"], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()