# Flodo Backend API 🚀

A high-performance Task Management API built with FastAPI and SQLAlchemy. This server manages task persistence, dependency logic ("Blocked-By"), and automated recurring task generation.

## 📝 Project Description
This backend serves as the core API for the Flodo Task Management application, built using FastAPI and SQLAlchemy. It provides endpoints for creating, retrieving, updating, deleting, and reordering tasks, along with advanced workflow features.

The system supports **task status management**, **dependency validation (Blocked-By logic)**, and **persistent drag-and-drop ordering**. It also includes **debounced search support via query parameters** and enforces business rules such as preventing completion of blocked tasks.

Additionally, the backend implements **asynchronous operations with a simulated 2-second latency** for task creation and updates, enabling realistic frontend testing. It also handles **recurring task automation**, where completing a recurring task triggers the creation of the next cycle while preserving the original task.

Designed with modular architecture (routes, schemas, CRUD, and database layers), the API ensures scalability, clean separation of concerns, and reliable database transactions.

## 🛠️ Tech Stack
* **Framework:** FastAPI (Standard)
* **ORM:** SQLAlchemy
* **Database:** PostgreSQL (via Psycopg2)
* **Language:** Python 3.9+

## ⚙️ Setup & Installation

### 1. Prerequisites & Cloning
Ensure you have Python installed. First, clone the repository:
```bash
git clone https://github.com/sristiacharya13/flodo_backend.git
cd flodo_backend
```
### 2. Environment Setup
Create and activate your virtual environment:
```bash
# 1. Create the Virtual Environment
python -m venv venv

# 2. Activate it (Windows)
.\venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install "Bridge" Libraries
```bash
pip install "fastapi[standard]" sqlalchemy psycopg2-binary
```

### 4. Database & .env Configuration
* **Create the Database:** Ensure your PostgreSQL server is running and create a database named flodo_db.
* **Setup .env:** Create a .env file in the root directory and add your connection string:
  ```bash
  DATABASE_URL=postgresql://user:password@localhost/flodo_db
  ```

### 5. Run the Application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📡 API Documentation
Once the server is running, access:
```bash
http://192.168.1.5:8000/tasks/
```

## 📌 Core API Endpoints
### 📝 Tasks

| Method | Endpoint                  | Description                                      |
|--------|--------------------------|--------------------------------------------------|
| GET    | `/tasks/`                | Get all tasks (with optional status & search)    |
| POST   | `/tasks/`                | Create a new task (includes 2s delay)            |
| PUT    | `/tasks/{task_id}/status`| Update task status                               |
| PUT    | `/tasks/{task_id}`       | Update full task (title, description, etc.)      |
| PUT    | `/tasks/reorder`         | Reorder tasks (drag-and-drop persistence)        |
| DELETE | `/tasks/{task_id}`       | Delete a task                                    |

## 🎯 Track A & Stretch Goals
* **Debounced Autocomplete Search:** Implemented debounced autocomplete search (300ms delay) with real-time filtering and highlighted matches in task titles.
* **Recurring Tasks Logic:** Built recurring task logic to auto-generate the next task cycle upon completion while preserving the original record.
* **Persistent Drag-and-Drop:** Enabled persistent drag-and-drop task reordering with database synchronization.

## 🧠 AI Implementation & Development Report
**Agents used**
* **Google Gemini:** Used for complex logic synchronization, Flutter Provider state management, and debugging race conditions.
* **Kilo Code (Grok Code Fast 1):** Utilized for initial boilerplate generation and UI component structuring.
  
### **The "Source of Truth" Method**
To prevent AI hallucinations and ensure "Elite" feature compliance, I provided the `assignment_logic.md` file as the primary grounding document.
**Core Instruction:** "Analyze the `assignment_logic.md` file in the root directory. All implementation including the 2-second simulated latency, debounced search, and recurring task logic must adhere strictly to these rules before proposing architecture."

### AI Usage and Debugging
**Prompts that gave me the most helpful code**
* "The 2-second delay is making my Save button clickable twice. How do we lock the UI in Flutter so the user can't spam the 'Create' button during that window?"
* "On Recurring Tasks: "The backend created the new task, but it’s not showing up in the app list immediately. Should I wait for the backend to finish its 'sleep' before I trigger the fetch call in Flutter?"

**Where the AI failed**
* **Conflict:** Gemini suggested using a decimal (+ 0.1) for the task position in the database. I noticed my models.py had position set as an Integer. I knew the database would just round 1.1 down to 1, which would break the reordering logic.
* **Fix:** I rejected the AI's suggestion and forced a whole-number increment (position + 1), ensuring every new recurring task has a unique, predictable spot in the list.