from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import TaskCreate, TaskResponse, TaskUpdate, ErrorResponse, TaskListResponse
from app.services import tasks as tasks_service

router = APIRouter(prefix="/tasks")


# -------------------------
# Tasks (Collection)
# -------------------------

@router.post(
    "/",
    tags=["Tasks (Collection)"],
    operation_id="tasks_create",
    response_model=TaskResponse,
    status_code=201,
    summary="Create a task",
    description="Creates a new task and returns it.",
    responses={
        422: {"model": ErrorResponse, "description": "Validation error."},
        500: {"model": ErrorResponse, "description": "Unexpected server error."},
    },
)
def create_task_route(
    payload: TaskCreate = Body(
        ...,
        examples={
            "simple": {
                "summary": "Simple task",
                "value": {"title": "Buy groceries", "description": "Milk, eggs, bread"},
            },
            "work": {
                "summary": "Work task",
                "value": {"title": "Prepare report", "description": "Quarterly summary"},
            },
        },
    ),
    db: Session = Depends(get_db),
):
    return tasks_service.create_task(db, payload)

@router.get(
    "/",
    tags=["Tasks (Collection)"],
    operation_id="tasks_list",
    response_model=TaskListResponse,
    summary="List tasks",
    description="Returns a paginated list of tasks.",
    responses={
        422: {"model": ErrorResponse, "description": "Validation error."},
        500: {"model": ErrorResponse, "description": "Unexpected server error."},
    },
)

def list_tasks_route(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=100, description="Max number of items to return.", examples=[50]),
    offset: int = Query(default=0, ge=0, description="Number of items to skip.", examples=[0]),
    done: bool | None = Query(default=None, description="Filter by completion status.", examples=[False]),
):
    items, total = tasks_service.list_tasks(db, limit=limit, offset=offset, done=done)
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "done": done,
    }

# -------------------------
# Tasks (Item)
# -------------------------

@router.get(
    "/{task_id}",
    tags=["Tasks (Item)"],
    operation_id="tasks_get",
    response_model=TaskResponse,
    summary="Get task by id",
    description="Returns a single task by its identifier.",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Task not found.",
            "content": {
                "application/json": {
                    "example": {"code": "TASK_NOT_FOUND", "message": "Task not found.", "details": {"task_id": 123}}
                }
            },
        },
        422: {"model": ErrorResponse, "description": "Validation error."},
        500: {"model": ErrorResponse, "description": "Unexpected server error."},
    },
)
def get_task_route(
    task_id: int = Path(..., ge=1, description="Task id.", examples=[1]),
    db: Session = Depends(get_db),
):
    task = tasks_service.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "TASK_NOT_FOUND", "message": "Task not found.", "details": {"task_id": task_id}},
        )
    return task


@router.patch(
    "/{task_id}",
    tags=["Tasks (Item)"],
    operation_id="tasks_update_status",
    response_model=TaskResponse,
    summary="Update task status",
    description="Updates the task done/undone status.",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found."},
        422: {"model": ErrorResponse, "description": "Validation error."},
        500: {"model": ErrorResponse, "description": "Unexpected server error."},
    },
)
def update_task_route(
    task_id: int = Path(..., ge=1, description="Task id.", examples=[1]),
    payload: TaskUpdate = Body(
        ...,
        examples={
            "mark_done": {"summary": "Mark as done", "value": {"done": True}},
            "mark_undone": {"summary": "Mark as undone", "value": {"done": False}},
        },
    ),
    db: Session = Depends(get_db),
):
    task = tasks_service.update_task_done(db, task_id, payload.done)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "TASK_NOT_FOUND", "message": "Task not found.", "details": {"task_id": task_id}},
        )
    return task


@router.delete(
    "/{task_id}",
    tags=["Tasks (Item)"],
    operation_id="tasks_delete",
    status_code=204,
    summary="Delete a task",
    description="Deletes a task by id.",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found."},
        422: {"model": ErrorResponse, "description": "Validation error."},
        500: {"model": ErrorResponse, "description": "Unexpected server error."},
    },
)
def delete_task_route(
    task_id: int = Path(..., ge=1, description="Task id.", examples=[1]),
    db: Session = Depends(get_db),
):
    deleted = tasks_service.delete_task(db, task_id)
    if deleted is False or deleted is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "TASK_NOT_FOUND", "message": "Task not found.", "details": {"task_id": task_id}},
        )
    return
