from pydantic import BaseModel, Field
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TaskCreate(BaseModel):

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    done: bool
    created_at: datetime

class TaskUpdate(BaseModel):

    model_config = ConfigDict(extra="forbid")
    
    done: bool



