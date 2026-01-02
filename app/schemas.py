from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class ErrorResponse(BaseModel):
    """
    Padrão único de erro para a API (aparece bonito no Swagger).
    """
    code: str = Field(
        ...,
        description="Stable application error code.",
        examples=["TASK_NOT_FOUND", "VALIDATION_ERROR", "DB_ERROR"],
    )
    message: str = Field(
        ...,
        description="Human-readable error message.",
        examples=["Task not found."],
    )
    details: dict[str, Any] | None = Field(
        default=None,
        description="Optional extra details to help debugging/clients.",
        examples=[{"task_id": 123}],
    )


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Short task title.",
        examples=["Buy groceries"],
    )
    description: str | None = Field(
        default=None,
        max_length=500,
        description="Optional task description.",
        examples=["Milk, eggs, bread."],
    )


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Task identifier.", examples=[1])
    title: str = Field(..., description="Short task title.", examples=["Buy groceries"])
    description: str | None = Field(
        default=None,
        description="Optional task description.",
        examples=["Milk, eggs, bread."],
    )
    done: bool = Field(False, description="Task completion status.", examples=[False])
    created_at: datetime = Field(..., description="Creation timestamp (UTC).")


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    done: bool = Field(
        ...,
        description="Mark task as done/undone.",
        examples=[True],
    )


