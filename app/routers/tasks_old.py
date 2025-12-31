from fastapi import APIRouter
from datetime import datetime, timezone
from app.schemas import TaskCreate, TaskResponse


router = APIRouter(prefix="/tasks", tags=["Tasks"])

# "Banco" em memória (só para aprender schema + router)
_tasks: list[TaskResponse] = []
_next_id = 1


@router.post("/", response_model=TaskResponse)
def create_task(payload: TaskCreate):
    global _next_id

    task = TaskResponse(
        id=_next_id,
        title=payload.title,
        description=payload.description,
        done=False,
        created_at=datetime.now(timezone.utc),
    )

    _tasks.append(task)
    _next_id += 1
    return task


@router.get("/", response_model=list[TaskResponse])
def list_tasks():
    return _tasks
