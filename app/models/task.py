from datetime import datetime

from fastapi.params import Depends, Query
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import Optional, Annotated


class TaskBase(SQLModel):
    description: str = Field(max_length=300)
    status: int

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creation_date: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    description: Optional[str] = Field(max_length=300)
    status: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    creation_date: datetime
    updated_at: datetime


class Pagination(BaseModel):
    offset: int
    limit: int

def pagination_params(
        offset: int = Query(2, ge=2, description="min list of task"),
        limit: int = Query(10, ge=10, description="max list of task"),
) -> Pagination:
    return Pagination(offset=offset, limit=limit)

PaginationDep = Annotated[Pagination, Depends(pagination_params)]