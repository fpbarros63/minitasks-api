from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import SessionLocal
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.services import tasks as tasks_service

from fastapi import Query

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TaskResponse)
def create_task_route(payload: TaskCreate, db: Session = Depends(get_db)):
    # Service retorna ORM; response_model + from_attributes converte para schema
    return tasks_service.create_task(db, payload)


@router.get("/", response_model=list[TaskResponse])
def list_tasks_route(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return tasks_service.list_tasks(db, limit=limit, offset=offset)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_route(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    return tasks_service.update_task_done(db, task_id, payload.done)

@router.delete("/{task_id}", status_code=204)
def delete_task_route(task_id: int, db: Session = Depends(get_db)):
    tasks_service.delete_task(db, task_id)
    return

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_route(task_id: int, db: Session = Depends(get_db)):
    return tasks_service.get_task_by_id(db, task_id)