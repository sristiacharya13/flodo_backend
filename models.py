import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base

class TaskStatus(str, enum.Enum):
    TODO = "To-Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class RecurringType(str, enum.Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=False) # Required Field
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO) # Required Field

    # Track A: Blocked By logic
    blocked_by_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    blocked_by = relationship("Task", remote_side=[id])

    # New fields for Elite Requirements
    position = Column(Integer, nullable=False, default=0)
    is_recurring = Column(Boolean, default=False)
    recurring_type = Column(Enum(RecurringType), nullable=True)