from datetime import datetime
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from auth.auth import requires_auth

from database.models import setup_db
from database.models import Author
from database.models import Book

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app, resources={r"/*": {"origins": "*"}})

  def validate_date(date_string):

    if date_string is None:
      return False

    try:
      datetime.strptime(date_string, '%Y/%m/%d')
      return True
    except ValueError:
      return False

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Methods',
                            'GET, POST, PATCH, DELETE, OPTIONS')
      return response

  @app.route('/')
  def test():
    return jsonify({'status': 'Running...'}), 200

  @app.route('/authors', methods=['GET'])
  @requires_auth("get:authors")
  def get_authors():
    authors_data = Author.query.all()

    authors = [author.short() for author in authors_data]

    return jsonify({
      "success": True,
      "authors": authors
    }), 200

  @app.route('/books', methods=['GET'])
  @requires_auth("get:books")
  def get_books():
    books_data = Book.query.all()

    books = [book.short() for book in books_data]

    return jsonify({
      "success": True,
      "books": books
    }), 200

  @app.route('/books/author/<int:author_id>', methods=['GET'])
  @requires_auth("get:books_by_author")
  def get_books_by_author(author_id):
    author = Author.query.get(author_id)

    if author is None:
      return abort(404)

    books = [book.short() for book in author.books]

    return jsonify({
      "success": True,
      "books": books
    }), 200

  @app.route('/authors/<int:author_id>', methods=['GET'])
  @requires_auth("get:authors_detail")
  def get_author_detail(author_id):
    existed_author = Author.query.get(author_id)

    if existed_author is None:
      return abort(404)

    return jsonify({
      "success": True,
      "authors": [existed_author.long()]
    }), 200

  @app.route('/books/<int:book_id>', methods=['GET'])
  @requires_auth("get:books_detail")
  def get_book_detail(book_id):
    existed_book = Book.query.get(book_id)

    if existed_book is None:
      return abort(404)

    return jsonify({
      "success": True,
      "books": [existed_book.long()]
    }), 200

  @app.route('/authors', methods=['POST'])
  @requires_auth("post:authors")
  def post_authors():
    body = request.get_json()

    name = body.get('name', "")
    full_name = body.get('full_name', "")
    dob = body.get('dob')

    if not validate_date(dob) or name.strip() == "" \
      or full_name.strip() == "":
      return abort(400)

    try:
      author = Author(name, full_name, dob)
      author.insert()
      
      return jsonify({
        "success": True,
        "authors": [author.long()]
      }), 200
    except Exception as e:
      print(e)
      abort(422)

  @app.route('/books', methods=['POST'])
  @requires_auth("post:books")
  def post_books():
    body = request.get_json()

    title = body.get('title', "")
    description = body.get('description')
    release_date = body.get('release_date')
    author_id = body.get('author_id')

    if not validate_date(release_date) or title.strip() == "" \
      or author_id is None:
      return abort(400)
    
    author = Author.query.get(author_id)

    if author is None:
      return abort(400)

    try:

      book = Book(title, description, release_date, author_id)
      book.insert()

      return jsonify({
        "success": True,
        "books": [book.long()]
      })
    
    except Exception as e:
      print(e)
      abort(422)

  @app.route('/books/<int:book_id>', methods=['PATCH'])
  @requires_auth("patch:books")
  def edit_book(book_id):
    book = Book.query.get(book_id)

    if book is None:
      abort(404)

    body = request.get_json()

    title = body.get('title', None)
    description = body.get('description', None)
    release_date = body.get('release_date', None)
    author_id = body.get('author_id', None)

    if release_date is not None and not validate_date(release_date):
      return abort(400)
    
    if author_id is not None:
      author = Author.query.get(author_id)

      if author is None:
        return abort(400)

    try:

      if title is not None:
        book.title = title

      if description is not None:  
        book.description = description

      if release_date is not None:
        book.release_date = release_date

      if author_id is not None:
        book.author_id = author_id

      book.update()

      return jsonify({
        "success": True,
        "books": [book.long()]
      })

    except Exception as e:
      print(e)
      abort(422)

  @app.route('/authors/<int:author_id>', methods=['PATCH'])
  @requires_auth("patch:authors")
  def edit_author(author_id):
    author = Author.query.get(author_id)

    if author is None:
      abort(404)

    body = request.get_json()

    name = body.get('name', None)
    full_name = body.get('full_name', None)
    dob = body.get('dob', None)

    if dob is not None and not validate_date(dob):
      return abort(400)

    try:
      
      if name is not None:
        author.name = name

      if full_name is not None:
        author.full_name = full_name

      if dob is not None:
        author.dob = dob

      author.update()
      
      return jsonify({
        "success": True,
        "authors": [author.long()]
      }), 200
    except Exception as e:
      print(e)
      abort(422)

  @app.route('/authors/<int:author_id>', methods=['DELETE'])
  @requires_auth("delete:authors")
  def delete_author(author_id):
    author = Author.query.get(author_id)

    if author is None:
      abort(404)
    
    try:
      author.delete()
      return jsonify({
        "success": True,
        "authors": [author_id]
      }), 200
    except Exception as e:
      print(e)
      abort(422)

  @app.route('/books/<int:book_id>', methods=['DELETE'])
  @requires_auth("delete:books")
  def delete_book(book_id):
    book = Book.query.get(book_id)

    if book is None:
      abort(404)
    
    try:
      book.delete()
      return jsonify({
        "success": True,
        "books": [book_id]
      }), 200
    except Exception as e:
      print(e)
      abort(422)

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource Not Found"
      }), 404

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request"
      }), 400

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable"
      }), 422

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "Method Not Allowed"
      }), 405

  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal Server Error"
      }), 500

  return app

app = create_app()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)