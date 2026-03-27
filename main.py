from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(status: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_tasks(db, status=status)

@app.put("/tasks/{task_id}/status")
def update_status(task_id: int, status: schemas.TaskStatus, db: Session = Depends(get_db)):
    result = crud.update_task_status(db, task_id=task_id, new_status=status)
    if result == "BLOCKED":
        raise HTTPException(status_code=400, detail="Cannot complete: This task is still blocked by another task.")
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result