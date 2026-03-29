# Flask + SQLAlchemy Task Manager REST API

A RESTful API for managing tasks built with Flask and SQLAlchemy.

## Setup

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd task-manager`
3. Create a virtual environment: `python -m venv .venv`
4. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/Mac: `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run the application: `python app.py`

## API Endpoints

### POST /api/tasks
Create a new task.

**Request Body:**
```json
{
  "title": "Task Title",
  "description": "Task Description",
  "status": "pending"
}
```

**Response (201):**
```json
{
  "id": 1,
  "title": "Task Title",
  "description": "Task Description",
  "status": "pending",
  "created_at": "2023-01-01T00:00:00Z"
}
```

### GET /api/tasks
Retrieve all tasks with pagination.

**Query Parameters:**
- `page` (integer, default: 1)
- `per_page` (integer, default: 5)

**Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Task Title",
      "description": "Task Description",
      "status": "pending",
      "created_at": "2023-01-01T00:00:00Z"
    }
  ],
  "page": 1,
  "per_page": 5,
  "total": 1
}
```

### PUT /api/tasks/<id>
Update a task's status.

**Request Body:**
```json
{
  "status": "completed"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Task Title",
  "description": "Task Description",
  "status": "completed",
  "created_at": "2023-01-01T00:00:00Z"
}
```

### DELETE /api/tasks/<id>
Delete a task.

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

## PowerShell Commands

### Create Task
```
Invoke-RestMethod -Method Post -Uri 'http://localhost:5000/api/tasks' `
  -Headers @{ 'Content-Type' = 'application/json' } `
  -Body '{"title": "Learn Flask", "description": "Build a REST API", "status": "pending"}'
```

### Get All Tasks
```
Invoke-RestMethod -Method Get -Uri 'http://localhost:5000/api/tasks?page=1&per_page=5'
```

### Update Task
```
Invoke-RestMethod -Method Put -Uri 'http://localhost:5000/api/tasks/1' `
  -Headers @{ 'Content-Type' = 'application/json' } `
  -Body '{"status": "completed"}'
```

### Delete Task
```
Invoke-RestMethod -Method Delete -Uri 'http://localhost:5000/api/tasks/1'
```

## Database

The application uses SQLite as the default database (`tasks.db` in the project root). To use a different database (e.g., MySQL), set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="mysql://user:password@localhost/taskdb"
```

## Docker

Build and run the application using Docker:

```bash
docker build -t task-manager .
docker run -p 5000:5000 task-manager
```

## Bonus Features

- **Pagination**: Supports paginated responses for the GET /api/tasks endpoint.
- **Input Validation**: Validates required fields and status values.
- **Docker Support**: Containerized deployment with Dockerfile.
