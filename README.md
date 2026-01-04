# MiniTasks API

MiniTasks API is a professional RESTful backend service designed to manage tasks in a clean, scalable, and well-documented way.

🎯 Project Goal

The project was built as a portfolio piece to demonstrate senior-level backend engineering practices, including RESTful API design, pagination, filtering, error handling, clean architecture, documentation quality and Docker-based deployment.

---

## ✨ Features

- Full CRUD operations for tasks
- RESTful design with clear resource boundaries (collection vs item)
- Professional pagination (`items`, `total`, `limit`, `offset`)
- Optional filtering (`done=true|false`)
- Consistent and structured error responses
- OpenAPI / Swagger documentation
- Dockerized environment for easy setup
- Clear separation of concerns (router / service / model)

---

## 🧱 Architecture

app/
├── main.py # Application entrypoint
├── models.py # SQLAlchemy ORM models
├── schemas.py # Pydantic schemas (API contracts)
├── database.py # Database configuration
├── exceptions.py # Custom exceptions and handlers
├── routers/
│ ├── tasks.py # Task endpoints (REST)
│ └── health.py # Health check
└── services/
└── tasks.py # Business logic (service layer)


### Why this structure?

- Routers handle HTTP and request/response concerns only  
- Services encapsulate business rules and logic  
- Models map database entities  
- Schemas define explicit API contracts  

This separation improves testability, readability, and long-term maintainability, and mirrors patterns commonly used in production-grade backend systems.

---

## 🌐 REST Design

The API follows REST principles by explicitly separating resources into:

### Collection

/tasks

Used to:
- Create tasks
- List tasks (with pagination and optional filters)

### Item

/tasks/{task_id}

Used to:
- Retrieve a single task
- Update task status
- Delete a task

This separation keeps endpoints predictable, expressive, and scalable as the API evolves.

---

## 📦 Pagination

The `GET /tasks` endpoint returns a paginated response designed for frontend and client consumption:

```json
{
  "items": [...],
  "total": 3,
  "limit": 2,
  "offset": 0,
  "done": null
}

Query parameters

limit: maximum number of items returned

offset: number of items skipped

done: optional filter (true or false)

Pagination metadata is always returned alongside the data, making the API easy to integrate with UI components.

## Error Handling

Errors follow a consistent structure across the API:

{
  "code": "TASK_NOT_FOUND",
  "message": "Task not found.",
  "details": {
    "task_id": 123
  }
}

This format ensures predictable client-side handling and clear error semantics.

## Running the project

Using Docker (recommended):

docker compose up --build

The API will be available at:

http://127.0.0.1:8000

Swagger UI:

http://127.0.0.1:8000/docs


## Example Requests

List tasks:

curl "http://127.0.0.1:8000/tasks?limit=2&offset=0"


Filter pending tasks:

curl "http://127.0.0.1:8000/tasks?done=false"


Create a task:

curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Study ML", "description": "Twice a week"}'

## Tech Stack

Python 3.12
FastAPI
SQLAlchemy
Pydantic
SQLite (development)
Docker & Docker Compose
