# MiniTasks API

Backend API for task management, built with FastAPI, SQLAlchemy, and Alembic,
focusing on clean architecture, database versioning, and long-term maintainability.

---

## Context

This project was developed to demonstrate professional backend engineering
practices commonly used in production systems.

The focus is not on feature quantity, but on architectural clarity,
schema evolution, testability, and reliability over time.

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Alembic
- SQLite (development and testing)
- Pytest

The project is designed to be easily adapted to PostgreSQL in production
environments.

---

## Architecture Highlights

- Database schema is **versioned exclusively via Alembic**
- Baseline migration strategy to align existing databases with version control
- Incremental, reversible migrations
- Clear separation of concerns:
  - Routers: HTTP layer
  - Services: business logic
  - Models: persistence
- Explicit configuration management
- Isolated test database to ensure reproducibility

---

## Database Migrations

All structural changes to the database schema are managed via Alembic.

Typical workflow:

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
