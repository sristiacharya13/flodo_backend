from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "To-Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class RecurringType(str, Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"

class TaskBase(BaseModel):
    title: str
    description: str # Requirement says "Text string", making it mandatory
    due_date: datetime
    status: TaskStatus = TaskStatus.TODO
    blocked_by_id: Optional[int] = None
    position: int = 0
    is_recurring: bool = False
    recurring_type: Optional[RecurringType] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True