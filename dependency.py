from sqlalchemy.orm import Session

from model import Task

def db_get_task(db: Session, task_id: int) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()

def db_get_all_task(db: Session) -> list[Task]:
    return db.query(Task).all()

def db_get_task_by_status(db: Session, status: str) -> list[Task]:
    return db.query(Task).filter(Task.status == status).all()

def db_create_task(db: Session, task: Task) -> Task:
    db.add(task)
    db.commit()
    db.refresh(task)
    return task