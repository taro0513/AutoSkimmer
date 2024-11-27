from sqlalchemy.orm import Session

from model import Task

def get_task(db: Session, task_id: int) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()
