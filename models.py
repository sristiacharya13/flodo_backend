from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
# Note: We import Base directly from database.py in the same folder
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Track A Requirement: Task Dependency (Self-Referencing)
    # This allows a task to be "Blocked By" another task ID
    blocked_by_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    
    # This creates the link so Python understands the relationship
    blocked_by = relationship("Task", remote_side=[id])