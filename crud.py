from sqlalchemy.orm import Session
import models, schemas

# 1. READ: Get a single task by ID
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# 2. READ: Get all tasks (with optional Filtering by status)
def get_tasks(db: Session, skip: int = 0, limit: int = 100, status: str = None):
    query = db.query(models.Task)
    if status:
        query = query.filter(models.Task.status == status)
    return query.offset(skip).limit(limit).all()

# 3. CREATE: Save a new task
def create_task(db: Session, task: schemas.TaskCreate):
    actual_blocker = task.blocked_by_id if task.blocked_by_id and task.blocked_by_id > 0 else None
    db_task = models.Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status=task.status,
        blocked_by_id=actual_blocker
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# 4. UPDATE: Update task status (Track A Logic)
def update_task_status(db: Session, task_id: int, new_status: models.TaskStatus):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        return None
    
    # Track A Logic: If trying to mark as "Done", check if the blocker is done first
    if new_status == models.TaskStatus.DONE and db_task.blocked_by_id:
        blocker = db.query(models.Task).filter(models.Task.id == db_task.blocked_by_id).first()
        if blocker and blocker.status != models.TaskStatus.DONE:
            # We return a specific message or raise an error in the API layer
            return "BLOCKED"

    db_task.status = new_status
    db.commit()
    db.refresh(db_task)
    return db_task

# 5. DELETE: Remove a task
def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False