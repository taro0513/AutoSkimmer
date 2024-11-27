from fastapi import FastAPI
from scheduler import scheduler
from task.route import router as task_router
from database import get_db
from webex import WebexClient
from zoom import ZoomClient

app = FastAPI()
webex_client = WebexClient()
zoom_client = ZoomClient()

@app.on_event("startup")
def init_scheduler():
    scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

app.include_router(task_router)
