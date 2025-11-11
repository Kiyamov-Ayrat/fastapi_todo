from sqlmodel import select

from app.database.task import SessionDep
from app.models.task import Task, Status


def get_todo(session: SessionDep):
    statement = select(Task).where(Task.status == Status.todo)
    result = session.exec(statement)
    return result.all()

def get_complete(session: SessionDep):
    statement = select(Task).where(Task.status == Status.completed)
    result = session.exec(statement)
    return result.all()

def get_in_progress(session: SessionDep):
    statement = select(Task).where(Task.status == Status.in_progress)
    result = session.exec(statement)
    return result.all()