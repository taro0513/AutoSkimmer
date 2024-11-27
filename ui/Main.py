import streamlit
import subprocess
import pathlib
import streamlit as st
import requests

from schema import TaskResponseSchema, TaskStatusType
def api_call_get_tasks(
        status: TaskStatusType = TaskStatusType.upcoming):
    # return requests.get(f"http://localhost:8000/task?status={status.value}").json()
    return []

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
    room_id = streamlit.text_input("Meeting Room ID")
    room_type = streamlit.selectbox("Meeting Room Type", ["Webex", "Zoom"])
    room_password = streamlit.text_input("Meeting Room Password")
    layout = streamlit.selectbox("Layout", ["Grid(Speaker)", "Stack(Gallery)", "SideBySide(MultipleSpeaker)"])

    if streamlit.button("Apply"):
        response = requests.post("http://localhost:8000/task", json={
            "name": title,
            "room_type": room_type.lower(),
            "room_id": room_id,
            "start_time": start_time,
            "end_time": end_time,
            "username": username,
            "password": password,
            "email": email,
            "repeat": repeat,
            "layout": layout
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
    streamlit.text_input("Task Title*", value=task.name, disabled=True)
    streamlit.selectbox("Meeting Room Type*", [
        "Webex" if task.room.room_type == "webex" else "Zoom"
    ], disabled=True)
    streamlit.text_input("Meeting Room ID*", value=task.room.room_id, disabled=True)
    streamlit.date_input("Date*", value=task.start_time.date(), disabled=True)
    streamlit.time_input("Start Time*", value=task.start_time.time(), disabled=True)
    streamlit.time_input("End Time*", value=task.end_time.time(), disabled=True)
    streamlit.text_input("User Mame*", value=task.username, disabled=True)
    streamlit.text_input("Meeting Room Password", value="******", disabled=True)
    streamlit.text_input("Email", value=task.email, disabled=True)
    streamlit.checkbox("Repeat", value=task.repeat, disabled=True)


@streamlit.dialog("Edit task details")
def edit_task_details(task: TaskResponseSchema):
    title = streamlit.text_input("Task Title*", value=task.name, disabled=True)
    room_type = streamlit.selectbox("Meeting Room Type*", ["Webex", "Zoom"],
                                    index=0 if task.room.room_type == "webex" else 1)
    room_id = streamlit.text_input("Meeting Room ID*", value=task.room.room_id)
    date = streamlit.date_input("Date*", value=task.start_time.date())
    start_time = streamlit.time_input("Start Time*", value=task.start_time.time())
    end_time = streamlit.time_input("End Time*", value=task.end_time.time())
    username = streamlit.text_input("User Mame*", value=task.username)
    password = streamlit.text_input("Meeting Room Password", value="******")
    if password == "******":
        password = None
    email = streamlit.text_input("Email", value=task.email)
    repeat = streamlit.checkbox("Repeat", value=task.repeat)
    if streamlit.button("Apply"):
        streamlit.success("Task updated successfully")
        streamlit.rerun()


@streamlit.dialog("Duplicate task")
def duplicate_task(task: TaskResponseSchema):
    title = streamlit.text_input("Task Title*", value=f"{task.name} - duplicate")
    room_type = streamlit.selectbox("Meeting Room Type*", ["Webex", "Zoom"],
                                    index=0 if task.room.room_type == "webex" else 1)
    room_id = streamlit.text_input("Meeting Room ID*", value=task.room.room_id)
    date = streamlit.date_input("Date*", value=task.start_time.date())
    start_time = streamlit.time_input("Start Time*", value=task.start_time.time())
    end_time = streamlit.time_input("End Time*", value=task.end_time.time())
    username = streamlit.text_input("User Mame*", value=task.username)
    password = streamlit.text_input("Meeting Room Password")
    email = streamlit.text_input("Email", value=task.email)
    repeat = streamlit.checkbox("Repeat", value=task.repeat)

    start_time = f"{date} {start_time}"
    end_time = f"{date} {end_time}"

    if streamlit.button("Apply"):
        response = requests.post("http://localhost:8000/task", json={
            "name": title,
            "room_type": room_type.lower(),
            "room_id": room_id,
            "start_time": start_time,
            "end_time": end_time,
            "username": username,
            "password": password,
            "email": email,
            "repeat": repeat,
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
    create_new_section()

streamlit.header("Currently Recording")

currently_recording_task = api_call_get_recording_tasks()
currently_recording_task = [TaskResponseSchema(**task) for task in currently_recording_task]

if currently_recording_task:
    for task in currently_recording_task:
        expander = streamlit.expander(f"🔴 {task.name}")
        expander.text(f"Start Record At: {task.start_time}")
        expander.text(f"Possibly End Record At: {task.end_time}")

        col1, col2, col3 = expander.columns(3, gap="small")
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


else:
    streamlit.write("No task is currently recording")

streamlit.header("Upcoming Recordings")

upcoming_tasks = api_call_get_upcoming_tasks()
upcoming_tasks = [TaskResponseSchema(**task) for task in upcoming_tasks]
if upcoming_tasks:
    for task in upcoming_tasks:
        expander = streamlit.expander(f"🟡 {task.name}")
        expander.text(f"Start Record At: {task.start_time}")
        expander.text(f"Possibly End Record At: {task.end_time}")

        col1, col2, col3 = expander.columns(3, gap="small")
        with col1:
            if streamlit.button("Start Record Now", key=f"_button_recording_upcoming_record_now_{task.id}"):
                upgrade_plan()
        with col2:
            if streamlit.button("Edit", key=f"_button_recording_upcoming_edit_{task.id}"):
                edit_task_details(task)

        with col3:
            if streamlit.button("Delete", key=f"_button_recording_upcoming_delete_{task.id}"):
                requests.delete(f"http://localhost:8000/task/{task.id}")
                streamlit.cache_data.clear()
                streamlit.rerun()
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
                open_file_in_explorer(task.output_path)

        with col3:
            if streamlit.button("Upload Video to Drive", key=f"_button_recording_completed_delete_{task.id}"):
                upgrade_plan()

        with col4:
            if streamlit.button("Duplicate Task", key=f"_button_recording_completed_duplicate_{task.id}"):
                duplicate_task(task)
else:
    streamlit.write("No completed task")
