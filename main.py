from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, crud
from database import engine, get_db

# Automatically create/update tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flodo Task API")

@app.post("/tasks/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    # Mandatory 2-second delay happens inside this awaited call
    return await crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(
    status: Optional[str] = None, 
    search: Optional[str] = None, # For the Debounced Search Goal
    db: Session = Depends(get_db)
):
    # This remains sync because fetching the list shouldn't have a 2s delay
    return crud.get_tasks(db, status=status, search=search)

@app.put("/tasks/{task_id}/status", response_model=schemas.Task)
async def update_status(task_id: int, status: schemas.TaskStatus, db: Session = Depends(get_db)):
    result = await crud.update_task_status(db, task_id=task_id, new_status=status)
    
    if result == "BLOCKED":
        raise HTTPException(
            status_code=400, 
            detail="Cannot complete: This task is still blocked by another task."
        )
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

@app.put("/tasks/reorder")
async def reorder_tasks(positions: List[dict], db: Session = Depends(get_db)):
    """Requirement: Persistent Drag-and-Drop. Syncs new order to DB."""
    await crud.update_task_positions(db=db, position_updates=positions)
    return {"message": "Positions updated successfully"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Handles general task updates (Title, Description, etc.) from Flutter."""
    result = await crud.update_task_full(db, task_id=task_id, task_update=task)
    
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result