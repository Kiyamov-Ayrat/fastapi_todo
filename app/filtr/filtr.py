from typing import Optional

from sqlmodel import select

from app.database.task import SessionDep
from app.models.task import Task, Status, TaskResponse


def get_task_status(
        session: SessionDep,
        status: Optional[Status] = None) -> list[TaskResponse]:
    stmt = select(Task)
    if status:
        stmt = stmt.where(Task.status == status)
    result = session.execute(stmt)
    return result.scalars().all()
