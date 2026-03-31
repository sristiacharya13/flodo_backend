import asyncio
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas

# 1. READ: Get a single task by ID
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# 2. READ: Get all tasks (Added Search & Position Ordering)
def get_tasks(db: Session, skip: int = 0, limit: int = 100, status: str = None, search: str = None):
    query = db.query(models.Task)
    if status:
        query = query.filter(models.Task.status == status)
    if search:
        # Debounced Search Requirement: Search by Title
        query = query.filter(models.Task.title.ilike(f"%{search}%"))
    
    # Drag-and-Drop Requirement: Order by position
    return query.order_by(models.Task.position).offset(skip).limit(limit).all()

# 3. CREATE: Save a new task (Added 2s Delay & Auto-Position)
async def create_task(db: Session, task: schemas.TaskCreate):
    await asyncio.sleep(2) # Mandatory 2-second simulation delay
    
    # Find the next available position for Drag-and-Drop
    max_pos = db.query(func.max(models.Task.position)).scalar() or 0
    
    db_task = models.Task(
        **task.dict(exclude={'position'}),
        position=max_pos + 1
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# 4. UPDATE: Update task status (Added 2s Delay & Recurring Logic)
async def update_task_status(db: Session, task_id: int, new_status: models.TaskStatus):
    await asyncio.sleep(2) # Mandatory 2-second simulation delay
    
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        return None
    
    # Track A Logic: Blocked By dependency check
    if new_status == models.TaskStatus.DONE and db_task.blocked_by_id:
        blocker = db.query(models.Task).filter(models.Task.id == db_task.blocked_by_id).first()
        if blocker and blocker.status != models.TaskStatus.DONE:
            return "BLOCKED"

    # Recurring Tasks Logic: Auto-generate duplicate if marked Done
    if new_status == models.TaskStatus.DONE and db_task.is_recurring:
        # Calculate next due date
        delta = timedelta(days=1) if db_task.recurring_type == models.RecurringType.DAILY else timedelta(weeks=1)
        
        new_task = models.Task(
            title=db_task.title,
            description=db_task.description,
            due_date=db_task.due_date + delta,
            status=models.TaskStatus.TODO,
            is_recurring=True,
            recurring_type=db_task.recurring_type,
            position=db_task.position # Maintain relative order
        )
        db.add(new_task)

    db_task.status = new_status
    db.commit()
    db.refresh(db_task)
    return db_task

# 5. Drag-and-Drop Sync: Update multiple positions at once
async def update_task_positions(db: Session, position_updates: list):
    for update in position_updates:
        db.query(models.Task).filter(models.Task.id == update['id']).update({"position": update['position']})
    db.commit()
    return True

# 6. DELETE: Remove a task
def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False

async def update_task_full(db: Session, task_id: int, task_update: schemas.TaskCreate):
    """Requirement: Edit existing tasks with full data update."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if not db_task:
        return None

    # Optional: Add the 2s delay here if you want it consistent with Create/Status updates
    # await asyncio.sleep(2) 

    # Extract the data and update the DB model fields
    update_data = task_update.dict(exclude_unset=True)

    # If the edit request changes status to DONE, apply the same behavior
    # as the dedicated status endpoint (blocked-by check + recurring duplication).
    new_status = update_data.get("status")
    if new_status == models.TaskStatus.DONE and db_task.status != models.TaskStatus.DONE:
        if db_task.blocked_by_id:
            blocker = db.query(models.Task).filter(models.Task.id == db_task.blocked_by_id).first()
            if blocker and blocker.status != models.TaskStatus.DONE:
                return "BLOCKED"

        if db_task.is_recurring:
            delta = timedelta(days=1) if db_task.recurring_type == models.RecurringType.DAILY else timedelta(weeks=1)
            base_due_date = update_data.get("due_date", db_task.due_date)
            new_task = models.Task(
                title=update_data.get("title", db_task.title),
                description=update_data.get("description", db_task.description),
                due_date=base_due_date + delta,
                status=models.TaskStatus.TODO,
                is_recurring=True,
                recurring_type=update_data.get("recurring_type", db_task.recurring_type),
                position=db_task.position,
            )
            db.add(new_task)

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task