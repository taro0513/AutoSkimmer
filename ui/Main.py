import streamlit
import subprocess
import pathlib
import streamlit as st
import requests
import datetime

API_URL = "http://localhost:8000"

from schema import TaskResponseSchema, TaskStatusType
def api_call_get_tasks(
        status: TaskStatusType = TaskStatusType.upcoming):
    return requests.get(f"{API_URL}/task?status={status.value}").json()
    # return []

@st.cache_data
def api_call_get_complete_tasks(
        status: TaskStatusType = TaskStatusType.completed):
    return api_call_get_tasks(status)


@st.cache_data
def api_call_get_recording_tasks(
        status: TaskStatusType = TaskStatusType.recording):
    return api_call_get_tasks(status)


@st.cache_data
def api_call_get_upcoming_tasks(
        status: TaskStatusType = TaskStatusType.upcoming):
    return api_call_get_tasks(status)


def api_call_create_task(task: dict) -> requests.Response:
    return requests.post("http://localhost:8000/task", json=task)

def api_call_delete_task(task_id: int) -> requests.Response:
    return requests.delete(f"http://localhost:8000/task/{task_id}")

streamlit.set_page_config(
    page_title="Meeting Recorder",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def open_file_in_explorer(file_path):
    file_path = pathlib.Path(file_path).resolve()
    subprocess.Popen(f'explorer /select,"{file_path}"')


@streamlit.dialog("Create a new task")
def create_new_task():
    name = streamlit.text_input("Task Name*")
    username = streamlit.text_input("User Name")
    email = streamlit.text_input("Email")
    date = streamlit.date_input("Date*")
    start_time = streamlit.time_input("Start Time")
    end_time = streamlit.time_input("End Time")
    repeat = streamlit.checkbox("Repeat")
    repeat_interval_days = streamlit.number_input("Repeat Every N Days",1,100)
    repeat_until = streamlit.date_input("Repeat Until")
    room_id = streamlit.text_input("Meeting Room ID")
    room_type = streamlit.selectbox("Meeting Room Type", ["Webex", "Zoom"])
    room_password = streamlit.text_input("Meeting Room Password")
    layout = streamlit.selectbox("Layout", ["mode_a", "mode_b", "mode_c", "mode_d"])

    if streamlit.button("Apply"):
        repeat_until = f"{repeat_until} {start_time}"
        start_time = f"{date} {start_time}"
        end_time = f"{date} {end_time}"
        response = requests.post("http://localhost:8000/task", json={
            "name": name,
            "username": username,
            "email": email,
            "start_time": start_time,
            "end_time": end_time,
            "repeat": repeat,
            "repeat_interval_days": repeat_interval_days,
            "repeat_until": repeat_until,
            "room": {
                "room_id": room_id,
                "room_type": room_type,
                "password": room_password,
                "layout": layout
            }
        })

        if response.status_code != 200:
            streamlit.error("Failed to create task")
            streamlit.error(response.json())
        else:
            streamlit.success("Task created successfully")
            streamlit.cache_data.clear()
            streamlit.rerun()


@streamlit.dialog("Task Details")
def view_task_details(task: TaskResponseSchema):
    streamlit.text_input("Task Name*", value=task.name, disabled=True)
    streamlit.text_input("User Mame*", value=task.username, disabled=True)
    streamlit.text_input("Email", value=task.email, disabled=True)
    streamlit.date_input("Date*", value=task.start_time.date(), disabled=True)
    streamlit.time_input("Start Time*", value=task.start_time.time(), disabled=True)
    streamlit.time_input("End Time*", value=task.end_time.time(), disabled=True)
    streamlit.checkbox("Repeat", value=task.repeat, disabled=True)
    streamlit.text_input("Meeting Room ID*", value=task.room.room_id, disabled=True)
    streamlit.selectbox("Meeting Room Type", ["Webex", "Zoom"],
                                    index=0 if task.room.room_type == "Webex" else 1, disabled=True)
    streamlit.text_input("Meeting Room Password", value="******", disabled=True)
    streamlit.selectbox("Layout", ["mode_a", "mode_b", "mode_c", "mode_d"], index=
                        ["mode_a", "mode_b", "mode_c", "mode_d"].index(task.room.layout), disabled=True)



@streamlit.dialog("Edit task details")
def edit_task_details(task: TaskResponseSchema):
    name = streamlit.text_input("Task Name*", value=task.name)
    username = streamlit.text_input("User Mame*", value=task.username)
    email = streamlit.text_input("Email", value=task.email)
    date = streamlit.date_input("Date*", value=task.start_time.date())
    start_time = streamlit.time_input("Start Time*", value=task.start_time.time())
    end_time = streamlit.time_input("End Time*", value=task.end_time.time())
    repeat = streamlit.checkbox("Repeat", value=task.repeat)
    room_id = streamlit.text_input("Meeting Room ID*", value=task.room.room_id)
    room_type = streamlit.selectbox("Meeting Room Type", ["Webex", "Zoom"], 
                                    index=0 if task.room.room_type == "Webex" else 1)
    room_password = streamlit.text_input("Meeting Room Password")
    layout = streamlit.selectbox("Layout", ["mode_a", "mode_b", "mode_c", "mode_d"], 
                                 index= ["mode_a", "mode_b", "mode_c", "mode_d"].index(task.room.layout))

    if streamlit.button("Apply"):
        start_time = f"{date} {start_time}"
        end_time = f"{date} {end_time}"
        api_call_delete_task(task_id=task.id)
        response = requests.post("http://localhost:8000/task", json={
            "name": name,
            "username": username,
            "email": email,
            "start_time": start_time,
            "end_time": end_time,
            "repeat": repeat,
            "room": {
                "room_id": room_id,
                "room_type": room_type,
                "password": room_password,
                "layout": layout
            }
        })

        if response.status_code != 200:
            streamlit.error("Failed to update task")
            streamlit.error(response.json())
        else:
            streamlit.success("Task updated successfully")
            streamlit.cache_data.clear()
            streamlit.rerun()


@streamlit.dialog("Duplicate task")
def duplicate_task(task: TaskResponseSchema):
    name = streamlit.text_input("Task Name*", value=task.name)
    username = streamlit.text_input("User Mame*", value=task.username)
    email = streamlit.text_input("Email", value=task.email)
    date = streamlit.date_input("Date*", value=task.start_time.date())
    start_time = streamlit.time_input("Start Time*", value=task.start_time.time())
    end_time = streamlit.time_input("End Time*", value=task.end_time.time())
    repeat = streamlit.checkbox("Repeat", value=task.repeat)
    room_id = streamlit.text_input("Meeting Room ID*", value=task.room.room_id)
    room_type = streamlit.selectbox("Meeting Room Type", ["Webex", "Zoom"], 
                                    index=0 if task.room.room_type == "Webex" else 1)
    room_password = streamlit.text_input("Meeting Room Password")
    layout = streamlit.selectbox("Layout", ["mode_a", "mode_b", "mode_c", "mode_d"], 
                                 index= ["mode_a", "mode_b", "mode_c", "mode_d"].index(task.room.layout))

    if streamlit.button("Apply"):
        start_time = f"{date} {start_time}"
        end_time = f"{date} {end_time}"
        response = requests.post("http://localhost:8000/task", json={
            "name": name,
            "username": username,
            "email": email,
            "start_time": start_time,
            "end_time": end_time,
            "repeat": repeat,
            "room": {
                "room_id": room_id,
                "room_type": room_type,
                "password": room_password,
                "layout": layout
            }
        })

        if response.status_code != 200:
            streamlit.error("Failed to create task")
            streamlit.error(response.json())
        else:
            streamlit.success("Task created successfully")
            streamlit.cache_data.clear()
            streamlit.rerun()



@streamlit.dialog("UPGRADE YOUR PLAN")
def upgrade_plan():
    streamlit.write("Upgrade your plan to get access to this feature")
    if streamlit.button("Upgrade"):
        streamlit.success("Plan upgraded successfully")
        streamlit.rerun()


if streamlit.button("Add Task", help="Create a new recording task"):
    create_new_task()

streamlit.header("Currently Recording")

currently_recording_task = api_call_get_recording_tasks()
currently_recording_task = [TaskResponseSchema(**task) for task in currently_recording_task]

if currently_recording_task:
    for task in currently_recording_task:
        expander = streamlit.expander(f"🔴 {task.name}")
        expander.text(f"Start Record At: {task.start_time}")
        expander.text(f"Possibly End Record At: {task.end_time}")

        col1, col2, col3, col4 = expander.columns(4, gap="medium")
        with col1:
            if streamlit.button("View Details", key=f"_button_recording_current_view_details_{task.id}"):
                view_task_details(task)
        with col2:
            if streamlit.button("Stop Recording", key=f"_button_recording_current_stop_recording_{task.id}"):
                upgrade_plan()
        with col3:
            if streamlit.button("Expand Recording Time",
                                key=f"_button_recording_current_expand_recording_time_{task.id}"):
                upgrade_plan()
        with col4:
            if streamlit.button("Duplicate Task", key=f"_button_recording_recording_duplicate_{task.id}"):
                duplicate_task(task)


else:
    streamlit.write("No task is currently recording")

streamlit.header("Upcoming Recordings")

upcoming_tasks = api_call_get_upcoming_tasks()
upcoming_tasks = [TaskResponseSchema(**task) for task in upcoming_tasks]
if upcoming_tasks:
    for task in upcoming_tasks:
        now_time = datetime.datetime.now(datetime.UTC)
        if task.start_time < now_time:
            expander = streamlit.expander(f"🟡 {task.name} (此任務設定時間已過)")
        else:
            expander = streamlit.expander(f"🟡 {task.name}")
        expander.text(f"Start Record At: {task.start_time}")
        expander.text(f"Possibly End Record At: {task.end_time}")

        col1, col2, col3, col4 = expander.columns(4, gap="medium")
        with col1:
            if streamlit.button("Start Record Now", key=f"_button_recording_upcoming_record_now_{task.id}"):
                upgrade_plan()

        with col2:
            if streamlit.button("View", key=f"_button_recording_upcoming_edit_{task.id}"):
                edit_task_details(task)

        with col3:
            if streamlit.button("Delete", key=f"_button_recording_upcoming_delete_{task.id}"):
                api_call_delete_task(task.id)
                streamlit.cache_data.clear()
                streamlit.rerun()
        with col4:
            if streamlit.button("Duplicate Task", key=f"_button_recording_upcoming_duplicate_{task.id}"):
                duplicate_task(task)
        
else:
    streamlit.write("No upcoming task")

streamlit.header("Completed Recordings")
completed_tasks = api_call_get_complete_tasks()
completed_tasks = [TaskResponseSchema(**task) for task in completed_tasks]
if completed_tasks:
    for task in completed_tasks:
        expander = streamlit.expander(f"🟢 {task.name}")
        expander.text(f"Start Record At: {task.start_time}")
        expander.text(f"End Record At: {task.end_time}")
        expander.text(f"Output Path: {task.output_path}")

        col1, col2, col3, col4 = expander.columns(4, gap="medium")
        with col1:
            if streamlit.button("View Details", key=f"_button_recording_completed_record_now_{task.id}"):
                view_task_details(task)
        with col2:
            if streamlit.button("Open Video in Explorer", key=f"_button_recording_completed_edit_{task.id}"):
                try:
                    open_file_in_explorer(task.output_path)
                except Exception as e:
                    streamlit.error(e)

        with col3:
            if streamlit.button("Upload Video to Drive", key=f"_button_recording_completed_delete_{task.id}"):
                upgrade_plan()

        with col4:
            if streamlit.button("Duplicate Task", key=f"_button_recording_completed_duplicate_{task.id}"):
                duplicate_task(task)
else:
    streamlit.write("No completed task")
