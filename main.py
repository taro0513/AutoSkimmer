import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Query

from scheduler import scheduler
from database import get_db

from schema import TaskCreateSchema, TaskResponseSchema
from service import create_task, get_task, get_all_task, delete_task
from model import TaskStatusType

from client import obs_client
from custom_logger import logger

app = FastAPI()


@app.on_event("startup")
def init_scheduler():
    logger.info("Start scheduler")
    scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler():
    logger.info("Stop scheduler")
    scheduler.shutdown()


@app.post(
    path='/task',
    response_model=TaskResponseSchema
)
async def create_task_endpoint(
    task: TaskCreateSchema,
    db: Session = Depends(get_db)
):
    return create_task(db, task)

@app.get(
    path='/task/{task_id}',
    response_model=TaskResponseSchema
)
async def get_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db)
):
    return get_task(db, task_id)

@app.get(
    path='/task',
    response_model=list[TaskResponseSchema]
)
async def get_all_tasks_endpoint(
    status: TaskStatusType | None = Query(None),
    db: Session = Depends(get_db)
):
    return get_all_task(db, status)

@app.delete(
    path='/task/{task_id}',
)
async def delete_task_endpoint(
        task_id: int,
        db: Session = Depends(get_db)
):
    return delete_task(db, task_id)