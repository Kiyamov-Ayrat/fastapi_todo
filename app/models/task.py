from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional

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