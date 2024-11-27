import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, EmailStr, Field, validator, field_validator

from model import MeetingRoomType, TaskStatusType, MeetingRoomLayout


class RoomCreateSchema(BaseModel):
    room_id: str
    room_type: MeetingRoomType
    password: str | None = Field(None)
    layout: MeetingRoomLayout | None = Field(None)


class RoomResponseSchema(RoomCreateSchema):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class TaskCreateSchema(BaseModel):
    name: str
    username: str
    email: str | None = Field(None)
    start_time: datetime.datetime
    end_time: datetime.datetime
    repeat: bool
    room: RoomCreateSchema
    @validator('start_time', 'end_time', pre=True)
    def set_timezone(cls, v):
        if isinstance(v, str):
            dt = datetime.datetime.fromisoformat(v)
        elif isinstance(v, datetime):
            dt = v
        else:
            raise TypeError('start_time must be a datetime object or ISO format string')

        if dt.tzinfo is None:
            return dt.replace(tzinfo=ZoneInfo("Asia/Taipei"))
        else:
            return dt.astimezone(ZoneInfo("Asia/Taipei"))


class TaskResponseSchema(TaskCreateSchema):
    id: int
    status: TaskStatusType
    output_path: str | None = Field(None)
    created_at: datetime.datetime
    updated_at: datetime.datetime