# FastAPI Async Blog

## Requirements

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- asyncpg

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/fastapi_async_blog.git
   cd fastapi_async_blog
Create and activate a virtual environment:
bash
Copy code
python3.11 -m venv venv
source venv/bin/activate
Install the dependencies:
bash
Copy code
pip install -r requirements.txt
Create a PostgreSQL database and configure the connection in the config.py file.
Apply Alembic migrations to create the database schema:
bash
Copy code
alembic upgrade head
Running

To run your FastAPI application, execute the following command:

bash
Copy code
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
The application will be accessible at http://localhost:8000.
