# BOOKSTORE API

## Udacity's FSND-CAPSTONE

Heroku deployed link: https://bookstore-capstone.herokuapp.com/
Local link: http://localhost:8080/

## Let's start

### Run this project locally

This project require Python 3.x and PIP already attach it. Please see python docs and install it!

#### Create virtual environment

You can install directly dependencies on you PC, but recommend you should use virtual environment for Python project.

Running this commands for create virtual environment and install dependencies in this environment.

```
python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt
```

#### Install docker and create Postgres container

This project using docker-compose to create Postgres container.
Master username: postgres
Master password: password

```
docker-compose -f docker-compose.yml up -d
```

It also have dump file for restore data to you database.
Create your `bookstore` database in postgres and restore data by command:

```
psql -h 127.0.0.1 -U postgres bookstore < bookstore.psql
```

#### Setup local environment

Note that this project require some local environment varialbes.
You can run each export command separately in file `setup.sh`
Or run below commands:

```
chmod +x ./setup.sh
./setup.sh
```

#### Run project

You can run this project server by command:

```
python3 app.py
```

#### Test

To run unit test of this project, run this command:

```
python3 test_app.py
```

## API references

This app deployed in Heroku, you can visit it at URL: https://bookstore-capstone.herokuapp.com/

Authentication: This application requires authentication to perform various actions. All the endpoints require
various permissions, except the root endpoint, that are passed via the `Bearer` token.

The application has three different types of roles:

- Viewer
  Has only `get:books, get:authors, get:books_detail, get:authors_detail, get:books_by_author` permissions.

- Admin
  Has all permissions to interact with project APIs.

### GET: /

- To check status of this app is running or not
- Sample request:
  - `https://bookstore-capstone.herokuapp.com/`

<details>
<summary>Sample Response</summary>

```
{
    "status": "Running..."
}
```

</details>

#### GET /books
 - General
   - Get the list of all the books
   - requires `get:books` permission
 
 - Sample Request
   - `https://bookstore-capstone.herokuapp.com/books`

<details>
<summary>Sample Response</summary>

```
{
    "books": [
        {
            "id": 1,
            "title": "REST API Design Rulebook",
            "author": "Jack"
        },
        {
            "id": 2,
            "title": "RESTful Java Web Services",
            "author": "Tommy"
        }
    ],
    "success": true
}
```

</details>

#### GET /authors
 - General
   - Get the list of all the authors
   - requires `get:authors` permission
 
 - Sample Request
   - `https://bookstore-capstone.herokuapp.com/authors`

<details>
<summary>Sample Response</summary>

```
{
    "authors": [
        {
            "id": 1,
            "name": "Jack"
        },
        {
            "id": 2,
            "name": "Tommy"
        }
    ],
    "success": true
}
```

</details>

#### GET /books/author/<author_id>
 - General
   - Get the list books of author
   - requires `get:books_by_author` permission
 
 - Sample Request
   - `https://bookstore-capstone.herokuapp.com/books/author/1`

<details>
<summary>Sample Response</summary>

```
{
    "books": [
        {
            "id": 1,
            "title": "REST API Design Rulebook",
            "author": "Jack"
        },
        {
            "id": 2,
            "title": "RESTful Java Web Services",
            "author": "Tommy"
        }
    ],
    "success": true
}
```

</details>

#### GET /books/<book_id>
 - General
   - Get detail of the book
   - requires `get:books_detail` permission
 
 - Sample Request
   - `https://bookstore-capstone.herokuapp.com/books/1`

<details>
<summary>Sample Response</summary>

```
{
    "books": [
        {
            "id": 1,
            "title": "REST API Design Rulebook",
            "author": "Jack",
            "description": "REST API Design Rulebook description",
            "release_date": "2020/03/03"
        }
    ],
    "success": true
}
```

</details>

#### GET /authors/<author_id>
 - General
   - Get detail of the author
   - requires `get:authors_detail` permission
 
 - Sample Request
   - `https://bookstore-capstone.herokuapp.com/authors/1`

<details>
<summary>Sample Response</summary>

```
{
  "authors": [
      {
          "id": 1,
          "name": "Jack",
          "full_name": "Jack Borrow",
          "dob": "1968/09/08",
          "number_of_books": 4
      }
  ],
  "success": true
}
```

</details>

### POST /books
 - General
   - Create a book
   - requires `post:books` permission
 
 - Sample Request
   - `https://bookstore-capstone.herokuapp.com/books`
   - Request body:
   ```
    {
      "title": "REST API Design Rulebook",
      "author_id": 1,
      "description": "REST API Design Rulebook description",
      "release_date": "2020/03/03"
    }
   ```

<details>
<summary>Sample Response</summary>

```
{
  "books": [
    {
      "id": 1,
      "title": "REST API Design Rulebook",
      "author": "Jack",
      "description": "REST API Design Rulebook description",
      "release_date": "2020/03/03"
    }
  ],
  "success": true
}
```

</details>

### POST /authors
 - General
   - Create an author
   - requires `post:authors` permission
 
 - Sample Request
   - `https://bookstore-capstone.herokuapp.com/authors`
   - Request body:
   ```
    {
      "name": "Jack",
      "full_name": "Jack Borrow",
      "dob": "1968/09/08"
    }
   ```

<details>
<summary>Sample Response</summary>

```
{
  "authors": [
      {
        "id": 1,
        "name": "Jack",
        "full_name": "Jack Borrow",
        "dob": "1968/09/08",
        "number_of_books": 0
      }
  ],
  "success": true
}
```

</details>

### PATCH /books/<book_id>
 - General
   - Edit a book
   - requires `patch:books` permission
 
 - Sample Request
   - `https://bookstore-capstone.herokuapp.com/books/1`
   - Request body:
   ```
    {
      "title": "REST API Design Rulebook_edited",
    }
   ```

<details>
<summary>Sample Response</summary>

```
{
  "books": [
    {
      "id": 1,
      "title": "REST API Design Rulebook_edited",
      "author": "Jack",
      "description": "REST API Design Rulebook description",
      "release_date": "2020/03/03"
    }
  ],
  "success": true
}
```

</details>

### PATCH /authors/<author_id>
 - General
   - Edit an author
   - requires `patch:authors` permission
 
 - Sample Request
   - `https://bookstore-capstone.herokuapp.com/authors/1`
   - Request body:
   ```
    {
      "name": "Jack_edit",
      "full_name": "Jack Borrow",
      "dob": "1968/09/08"
    }
   ```

<details>
<summary>Sample Response</summary>

```
{
  "authors": [
      {
        "id": 1,
        "name": "Jack_edit",
        "full_name": "Jack Borrow",
        "dob": "1968/09/08",
        "number_of_books": 0
      }
  ],
  "success": true
}
```

</details>

#### DELETE /book/<book_id>
 - General
   - Delete a book
   - requires `delete:books` permission
 
 - Sample Request
   - `https://bookstore-capstone.herokuapp.com/books/1`

<details>
<summary>Sample Response</summary>

```
{
  "books": [1],
  "success": true
}
```

</details>

#### DELETE /authors/<author_id>
 - General
   - Delete an author
   - requires `delete:authors` permission
 
 - Sample Request
   - `https://bookstore-capstone.herokuapp.com/authors/1`

<details>
<summary>Sample Response</summary>

```
{
  "authors": [1],
  "success": true
}
```

</details>
