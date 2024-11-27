import datetime
from enum import StrEnum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.types import Boolean
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )


class MeetingRoomType(StrEnum):
    WEBEX = "Webex"
    ZOOM = "Zoom"


class TaskStatusType(StrEnum):
    recording = "recording"
    upcoming = "upcoming"
    completed = "completed"


class MeetingRoomLayout(StrEnum):
    GRID = "grid"
    STACK = "stack"
    SIDE_BY_SIDE = "side_by_side"
    SPEAKER = "speaker"
    GALLERY = "gallery"
    MULTIPLE_SPEAKER = "multiple_speaker"


class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True)
    start_time: Mapped[datetime.datetime] = mapped_column(String(50), nullable=False)
    end_time: Mapped[datetime.datetime] = mapped_column(String(50), nullable=False)
    repeat: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[TaskStatusType] = mapped_column(String, nullable=False, default=TaskStatusType.upcoming)
    output_path: Mapped[str] = mapped_column(String(100), nullable=True)
    room: Mapped["Room"] = relationship("Room", back_populates="task")


class Room(Base):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    room_id: Mapped[str] = mapped_column(String(50), nullable=False)
    room_type: Mapped[MeetingRoomType] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=True)
    layout: Mapped[MeetingRoomLayout] = mapped_column(String, nullable=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    task: Mapped["Task"] = relationship("Task", back_populates="room")
