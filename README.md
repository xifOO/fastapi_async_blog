## Async Blogging Application

---

***Welcome to the Blogging Application! 
This is an asynchronous web application developed in Python 3.11 using the FastAPI framework, PostgreSQL database system, and SQLAlchemy ORM library. 
Here you will find some important information about the project and instructions for installation and running.***

---

## Project Description

*The Blogging Application provides users with the ability to publish their posts and exchange comments. It is built on an asynchronous architecture, enabling efficient request handling and interaction with the database.*

Key technologies used in the project:

* ***Python 3.11***: **The programming language used for the application**.
* ***FastAPI***: **A powerful web framework for building APIs with Python, with built-in support for asynchronous operations**.
* ***PostgreSQL***: **A relational database management system**.
* ***SQLAlchemy***: **An ORM library for working with databases in Python**.

---

## Installation

**Before installing the application, please ensure that you have Python 3.11 and PostgreSQL installed on your system.**

Clone the repository to your local machine:

* ***git clone https://github.com/xifOO/fastapi_async_blog.git***

Create a virtual environment and activate it:

* ***python3 -m venv venv***
* ***source venv/bin/activate***  # for Unix/Linux
* ***venv\Scripts\activate***  # for Windows
* ***pip install -r requirements.txt***


Set up the environment variables:

Create a .env file in the root directory of the project.
In the .env file, set the following environment variables:

* ***POSTGRES_USER=your_user***
* ***POSTGRES_PASSWORD=your_password***
* ***POSTGRES_HOST=your_host***
* ***POSTGRES_PORT=your_port***
* ***POSTGRES_NAME=your_name***
* ***SECRET=your_secret_key*** # ***openssl rand -hex 32***
* ***ALGORITHM = your_algorithm***
* ***ACCESS_TOKEN_EXPIRE_MINUTES = your_access_token_expire_minutes***

Replace username, password, and database_name with your own PostgreSQL database connection details and algorithm encryption.

Run the database migrations:

* ***alembic upgrade head***

---

## Running the Application

After successful installation and setup, you can run the blogging application:

* ***uvicorn main:app --reload***

The application will be available at http://localhost:8000. You can open it in a web browser and start using it.
