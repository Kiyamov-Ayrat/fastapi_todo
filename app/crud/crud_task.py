from datetime import datetime

from fastapi import HTTPException

from app.database.task import SessionDep
from app.models.task import Task, TaskCreate, TaskUpdate


def create_tasks(task: TaskCreate, session: SessionDep):
    db_task = Task(
        description=task.description,
        status=task.status,
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_all_tasks(session: SessionDep):
    task_data = session.query(Task).all()
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
    updated_task = db_task.model_dump(exclude_unset=True)
    for field, value in updated_task.items():
        setattr(db_task, field, value)
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
    return {"Ok": True}
