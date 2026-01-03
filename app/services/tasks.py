from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate
from sqlalchemy.orm import Session
from app.models import Task
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions import NotFoundError

from typing import Optional, Tuple


def create_task(db: Session, data: TaskCreate) -> Task:
    task = Task(
        title=data.title,
        description=data.description,
        done=False,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task



def list_tasks(
    db: Session,
    limit: int = 50,
    offset: int = 0,
    done: Optional[bool] = None,
) -> tuple[list[Task], int]:
    q = db.query(Task)

    if done is not None:
        q = q.filter(Task.done == done)

    total = q.count()

    items = (
        q.order_by(Task.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return items, total

    

def update_task_done(db: Session, task_id: int, done: bool) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise NotFoundError("Task not found")

    task.done = done
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int) -> None:
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise NotFoundError("Task not found")

    try:
        db.delete(task)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        # Erro interno do banco/ORM (não é "erro do cliente")
        raise

def get_task_by_id(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise NotFoundError("Task not found")
    
    return task