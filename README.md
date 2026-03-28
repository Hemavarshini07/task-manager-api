# Task Manager API

A simple Flask + SQLAlchemy task manager backend.

## Setup

1. `git clone <repo>`
2. `cd task-manager` (or `cd "c:\Users\Hema\Documents\ds - assignment"`)
3. `python -m venv .venv`
4. `source .venv/Scripts/activate` (Windows PowerShell) or `source .venv/bin/activate` (Unix)
5. `pip install -r requirements.txt`
6. `python app.py`

## Endpoints (Base URL: `/api`)

- POST `/tasks`
  - body: `{ "title": "Learn Flask", "description": "Build API" }`
  - validation: title required, status optional (pending/completed)

- GET `/tasks`
  - params: `page` (default 1), `per_page` (default 5)

- PUT `/tasks/<id>`
  - body: `{ "status": "completed" }`

- DELETE `/tasks/<id>`

## Postman Example

- Create Task:
  - POST `/api/tasks`
  - body:
  ```json
  {
    "title": "Learn Flask",
    "description": "Build API"
  }
  ```

## Bonus

- Pagination: implemented via `GET /api/tasks?page=1&per_page=5`
- Input validation: title required and status strict checks

## Database

- Default: `sqlite:///tasks.db`
- Optional: set `DATABASE_URL` env var for MySQL or others

## Docker (optional)

1. `docker build -t task-manager .`
2. `docker run -p 5000:5000 task-manager`
