from sqlalchemy.orm import Session
from apscheduler.triggers.date import DateTrigger
import datetime
from zoneinfo import ZoneInfo
import time
from fastapi import HTTPException

from schema import TaskCreateSchema, TaskResponseSchema, RoomCreateSchema, RoomResponseSchema
from model import Room, Task, MeetingRoomType, TaskStatusType
from database import engine
from dependency import db_get_task, db_get_task_by_status, db_get_all_task
from scheduler import scheduler
from client import zoom_client, webex_client, obs_client
from watermark import WatermarkApp



def create_task(db: Session, task: TaskCreateSchema) -> TaskResponseSchema:
    room = Room(
        room_id=task.room.room_id,
        room_type=task.room.room_type,
        password=task.room.password,
        layout=task.room.layout,
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

    add_recording_job_to_scheduler(task, start_recording, task.start_time, "start_recording")
    add_recording_job_to_scheduler(task, stop_recording, task.end_time, "stop_recording")

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

def get_task(db: Session, task_id: int) -> TaskResponseSchema:
    task = db_get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

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

def get_all_task(db: Session, status: TaskStatusType | None = None) -> list[TaskResponseSchema]:
    if status:
        tasks = db_get_task_by_status(db, status)
    else:
        tasks = db_get_all_task(db)

    return [
        TaskResponseSchema(
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
        for task in tasks
    ]

def delete_task(db: Session, task_id: int):
    task = db_get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    remove_recording_job_from_scheduler(f"{task_id}-start_recording")
    remove_recording_job_from_scheduler(f"{task_id}-stop_recording")

    db.delete(task.room)
    db.delete(task)
    db.commit()

    return task_id

def add_recording_job_to_scheduler(
        task: Task, func: callable, run_date: datetime.datetime, job_id_suffix: str = None
):
    print(f"Add recording job to scheduler: {task.id} ({func.__name__})")
    print(f"Run date: {run_date}")
    print(f"Room ID: {task.room.room_id}")
    scheduler.add_job(
        func=func,
        trigger=DateTrigger(run_date, timezone=ZoneInfo("Asia/Taipei")),
        args=[task],
        id=f"{task.id}-{job_id_suffix}",
    )

def remove_recording_job_from_scheduler(job_id: str):
    print(f"Remove recording job from scheduler: {job_id}")
    scheduler.remove_job(job_id)

def wait_for(seconds: int):
    time.sleep(seconds)


def start_zoom_meeting(task: Task):
    wm = WatermarkApp("Zoom 錄影任務即將開始，請勿觸碰電腦。")
    wm.start()

    wait_for(10)
    obs_client.start()
    wait_for(10)
    obs_client.connect_to_server()
    wait_for(10)
    obs_client.set_recording_scene()

    print(f"Start Zoom meeting: {task.name} - {task.id}")
    zoom_client.shutdown()
    wait_for(10)
    zoom_client.start()
    wait_for(10)
    zoom_client.press_join_meeting_button()
    wait_for(10)
    zoom_client.type_meeting_information(task.room.room_id, task.username)
    wait_for(10)
    while True:
        zoom_client.reset_mouse_position()
        if zoom_client.wait_for_enter_password_window():
            break
        time.sleep(10)
        zoom_client.cancel_window()
        zoom_client.press_join_meeting_button()
        zoom_client.type_meeting_information(task.room.room_id, task.username)
    wait_for(10)
    zoom_client.type_meeting_password(task.room.password)
    wait_for(5)
    zoom_client.maximize_window()
    wait_for(10)
    zoom_client.press_layout_button_and_select_layout(task.room.layout)
    wait_for(10)
    zoom_client.open_chat_room()
    wait_for(5)
    zoom_client.move_chat_room_to_left_button()

    obs_client.start_record()

    wm.stop()
    del wm

def start_webex_meeting(task: Task):
    wm = WatermarkApp("Webex 錄影任務即將開始，請勿觸碰電腦。")
    wm.start()

    wait_for(10)
    obs_client.start()
    wait_for(10)
    obs_client.connect_to_server()
    wait_for(10)
    obs_client.set_recording_scene()

    print(f"Start Webex meeting: {task.name} - {task.id}")
    webex_client.shutdown()
    wait_for(10)
    webex_client.start()
    wait_for(10)
    webex_client.press_join_meeting_button()
    wait_for(10)
    webex_client.type_meeting_information(task.room.room_id)
    wait_for(10)
    while True:
        if webex_client.wait_for_ready_enter_window():
            break
        time.sleep(10)
        webex_client.cancel_window()
        webex_client.press_join_meeting_button()
        webex_client.type_meeting_information(task.room.room_id)
    # wait_for(10)
    # webex_client.type_meeting_password(task.room.password)
    # webex client does not need password
    wait_for(10)
    webex_client.enter_meeting()
    wait_for(10)
    webex_client.maximize_window()
    wait_for(10)
    webex_client.wait_for_enter_meeting()
    wait_for(10)
    webex_client.press_layout_button_and_select_layout(task.room.layout)
    wait_for(10)
    webex_client.open_chat_room()

    obs_client.start_record()

    wm.stop()
    del wm

def stop_zoom_meeting():
    obs_client.connect_to_server()
    obs_client.stop_record()


    zoom_client.stop()
    wait_for(10)
    zoom_client.shutdown()

def stop_webex_meeting():
    obs_client.connect_to_server()
    obs_client.stop_record()

    webex_client.stop()
    wait_for(10)
    webex_client.shutdown()

def start_recording(task: Task):
    print(f"Start recording task: {task.name} - {task.id} ...")

    with Session(engine) as db:
        db_task = db_get_task(db, task.id)
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
        db_task = db_get_task(db, task.id)
        db_task.status = TaskStatusType.completed
        db.commit()
        db.refresh(db_task)

    print(f"Recording task: {task.name} - {task.id} stop.")