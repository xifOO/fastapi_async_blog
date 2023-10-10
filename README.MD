# FastAPI Async Blog

## Requirements

- Python 3.11
- FastAPI 
- SQLAlchemy
- PostgreSQL
- Alembic
- asyncpg

## Installation

## Clone the repository:

**git clone https://github.com/fastapi_async_blog.git**
**cd fastapi_async_blog**

# Create and activate a virtual environment:

**python3.11 -m venv venv**
**source venv/bin/activate**

##Install the dependencies:

**pip install -r requirements.txt**

#Create a PostgreSQL database and configure the connection in the config.py file.
#Apply Alembic migrations to create the database schema:

**alembic upgrade head**


#To run your FastAPI application, execute the following command:

**uvicorn main:app --host 0.0.0.0 --port 8000 --reload**
**The application will be accessible at http://localhost:8000.**
