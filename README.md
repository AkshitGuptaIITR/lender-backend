# Lender Backend

## Setup

1. **Create Virtual Environment** (if not already done):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```

## Database

This project uses PostgreSQL. Make sure you have a PostgreSQL instance running and a database named `lender_db` created (or update `.env` to match your setup).

### Migrations (Alembic)

*   **Create a new migration** (after changing models):
    ```bash
    alembic revision --autogenerate -m "Description of changes"
    ```

*   **Apply migrations**:
    ```bash
    alembic upgrade head
    ```

## Running the App

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
*   Swagger UI: http://127.0.0.1:8000/docs
*   ReDoc: http://127.0.0.1:8000/redoc
