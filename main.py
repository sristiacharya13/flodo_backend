from fastapi import FastAPI
import models
from database import engine

# This line creates the tables in PostgreSQL automatically!
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Database Connected & Tables Created!"}