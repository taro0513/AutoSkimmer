from sqlalchemy.orm import Session
from apscheduler.triggers.date import DateTrigger
import datetime
from zoneinfo import ZoneInfo
import time

from scheme import TaskCreateSchema, TaskResponseSchema, RoomCreateSchema, RoomResponseSchema
from model import Room, Task, MeetingRoomType, TaskStatusType
from main import webex_client, zoom_client, scheduler
from database import engine
from task.dependency import get_task


async def create_task(db: Session, task: TaskCreateSchema,
                      obs_client, meeting_client) -> TaskResponseSchema:
    room = Room(
        room_id=task.room_id,
        room_type=task.room_type,
        password=task.password,
        layout=task.layout,
    )
    task = Task(
        name=task.name,
        username=task.username,
        email=task.email,
        start_time=task.start_time,
        end_time=task.end_time,
        repeat=task.repeat,
        room=room,
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    db.refresh(room)

    add_recording_job_to_scheduler(task, start_recording, task.start_time)
    add_recording_job_to_scheduler(task, stop_recording, task.end_time)

    return TaskResponseSchema(
        id=task.id,
        name=task.name,
        username=task.username,
        email=task.email,
        start_time=task.start_time,
        end_time=task.end_time,
        repeat=task.repeat,
        room=RoomResponseSchema(
            id=task.room.id,
            room_id=task.room.room_id,
            room_type=task.room.room_type,
            layout=task.room.layout,
            created_at=task.room.created_at,
            updated_at=task.room.updated_at,
        ),
        status=task.status,
        output_path=task.output_path,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


def add_recording_job_to_scheduler(
        task: Task, func: callable, run_date: datetime.datetime
):
    print(f"Add recording job to scheduler: {task.id}")
    print(f"Run date: {run_date}")
    print(f"Room ID: {task.room.room_id}")
    scheduler.add_job(
        func=func,
        trigger=DateTrigger(run_date, timezone=ZoneInfo("Asia/Taipei")),
        args=[task],
    )


def wait_for(seconds: int):
    time.sleep(seconds)


def start_zoom_meeting(task: Task):
    print(f"Start Webex meeting: {task.name} - {task.id}")
    zoom_client.shutdown()
    wait_for(10)
    zoom_client.start()
    wait_for(10)
    zoom_client.press_join_meeting_button()
    wait_for(10)
    zoom_client.type_meeting_information(task.room.room_id, task.username)
    wait_for(10)
    zoom_client.type_meeting_password(task.room.password)
    wait_for(10)
    zoom_client.maximize_window()
    wait_for(10)
    zoom_client.press_layout_button_and_select_layout(task.room.layout)

def start_webex_meeting(task: Task):
    print(f"Start Webex meeting: {task.name} - {task.id}")
    webex_client.shutdown()
    wait_for(10)
    webex_client.start()
    wait_for(10)
    webex_client.press_join_meeting_button()
    wait_for(10)
    webex_client.type_meeting_information(task.room.room_id)
    wait_for(10)
    webex_client.type_meeting_password(task.room.password)
    wait_for(10)
    webex_client.enter_meeting()
    wait_for(10)
    webex_client.maximize_window()
    wait_for(10)
    webex_client.wait_for_enter_meeting()
    wait_for(10)
    webex_client.press_layout_button_and_select_layout(task.room.layout)

def stop_zoom_meeting():
    zoom_client.stop()
    wait_for(10)
    zoom_client.shutdown()

def stop_webex_meeting():
    webex_client.stop()
    wait_for(10)
    webex_client.shutdown()
def start_recording(task: Task):
    print(f"Start recording task: {task.name} - {task.id} ...")

    with Session(engine) as db:
        db_task = get_task(db, task.id)
        db_task.status = TaskStatusType.recording
        db.commit()
        db.refresh(db_task)

    if task.room.room_type == MeetingRoomType.WEBEX:
        start_webex_meeting(task)
    elif task.room.room_type == MeetingRoomType.ZOOM:
        start_zoom_meeting(task)

    print(f"Recording task: {task.name} - {task.id} start.")

def stop_recording(task: Task):
    print(f"Stop recording task: {task.name} - {task.id} ...")

    if task.room.room_type == MeetingRoomType.WEBEX:
        stop_webex_meeting()
    elif task.room.room_type == MeetingRoomType.ZOOM:
        stop_zoom_meeting()

    with Session(engine) as db:
        db_task = get_task(db, task.id)
        db_task.status = TaskStatusType.completed
        db.commit()
        db.refresh(db_task)

    print(f"Recording task: {task.name} - {task.id} stop.")