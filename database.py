import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Replace 'YOUR_PASSWORD' with the one you set for PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DEBUG: SQLALCHEMY_DATABASE_URL = {SQLALCHEMY_DATABASE_URL}")

# The engine is the "bridge" to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# This creates a "Session" for every request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We will inherit from this 'Base' class to create our Models (Tables)
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()