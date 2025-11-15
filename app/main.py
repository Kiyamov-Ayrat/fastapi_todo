from typing import Optional

from fastapi import FastAPI, Query, status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.database.task import create_db_tables, SessionDep
from contextlib import asynccontextmanager
from app.crud import crud_task
from app.models.task import TaskResponse, TaskCreate, TaskUpdate, PaginationDep, Status
from app.filtr import filtr


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield
app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:63342",   # JetBrains browser
    "http://127.0.0.1",
    "http://127.0.0.1:63342",
    "*"  # можно убрать позже
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/tasks/", response_model=list[TaskResponse])
def get_tasks_status(session: SessionDep,
                     status: Optional[Status] = Query(None)
                     ):
    return filtr.get_task_status(session=session, status=status)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: SessionDep):
    return crud_task.create_tasks(task=task, session=session)

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(session: SessionDep, pagination: PaginationDep):
    return crud_task.get_all_tasks(session=session, pagination=pagination)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, session: SessionDep):
    return crud_task.get_by_id(task_id=task_id, session=session)

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, session: SessionDep):
    return crud_task.update_task(task_id=task_id, task=task, session=session)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: SessionDep):
    return crud_task.delete_task(task_id=task_id, session=session)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
