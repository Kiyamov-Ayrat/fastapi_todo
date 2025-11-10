from datetime import datetime

from fastapi import HTTPException
from sqlmodel import select
from starlette import status
from app.database.task import SessionDep
from app.models.task import Task, TaskCreate, TaskUpdate, Pagination


def create_tasks(task: TaskCreate, session: SessionDep):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_all_tasks(session: SessionDep, pagination: Pagination):
    task_data = session.exec(select(Task).offset(pagination.offset).limit(pagination.limit)).all()
    return task_data

def get_by_id(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def update_task(task: TaskUpdate,
                session: SessionDep,
                task_id: int):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(updated_task)
    db_task.updated_at = datetime.now()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return status.HTTP_202_ACCEPTED
