# Settler Backend

This is the backend for the Settler application, which provides authentication and other services using FastAPI and Supabase.

## Project Structure

```
settler-backend
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   ├── api
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── services
│   │   ├── __init__.py
│   │   └── supabase_client.py
│   └── schemas
│       ├── __init__.py
│       └── user.py
├── .env
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd settler-backend
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and add your Supabase URL and API keys:
   ```
   SUPABASE_URL=<your-supabase-url>
   SUPABASE_KEY=<your-supabase-key>
   ```

5. **Run the application:**
   ```
   uvicorn src.main:app --reload
   ```

## Usage

- The backend provides authentication routes for user registration, login, and token verification.
- You can access the API documentation at `http://localhost:8000/docs` after running the application.

## License

This project is licensed under the MIT License.