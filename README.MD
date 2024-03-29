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
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt

4. **Create a PostgreSQL database and configure the connection in the config.py file.**
   **Apply Alembic migrations to create the database schema:**

   ```bash
   alembic upgrade head

5. **To run your FastAPI application, execute the following command:**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
