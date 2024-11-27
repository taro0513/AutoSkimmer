from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from config import config

jobstores = {
    "default": SQLAlchemyJobStore(url=config.JOB_SCHEDULER_DB),
}
executors = {
    "default": ThreadPoolExecutor(20),
    "processpool": ProcessPoolExecutor(5),
}
job_defaults = {"coalesce": False, "max_instances": 3}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone="Asia/Taipei",
)