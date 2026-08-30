"""
Task API — a small CRUD API for managing a to-do list.
In-memory storage only (no database) — data resets on restart, on purpose.
Run: uvicorn main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A small in-memory CRUD API for managing a to-do list.",
)


# ---------- Models ----------

class Task(BaseModel):
    id: int
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    title: str = Field(..., description="The task title. Cannot be empty.")


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# ---------- In-memory "database" ----------

tasks: List[Task] = [
    Task(id=1, title="Buy milk", done=False),
    Task(id=2, title="Write README", done=False),
    Task(id=3, title="Ship the API", done=True),
]
next_id = 4


def find_task(task_id: int) -> Optional[Task]:
    return next((t for t in tasks if t.id == task_id), None)


# ---------- Stage 1: root and health ----------

@app.get("/", summary="API info")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Health check")
def health():
    return {"status": "ok"}


# ---------- Stage 2: read ----------

@app.get("/tasks", response_model=List[Task], summary="List all tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task, summary="Get a single task")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


# ---------- Stage 3: create ----------

@app.post("/tasks", response_model=Task, status_code=201, summary="Create a task")
def create_task(payload: TaskCreate):
    global next_id
    if not payload.title or not payload.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")
    task = Task(id=next_id, title=payload.title.strip(), done=False)
    tasks.append(task)
    next_id += 1
    return task


# ---------- Stage 4: update & delete ----------

@app.put("/tasks/{task_id}", response_model=Task, summary="Update a task")
def update_task(task_id: int, payload: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    if payload.title is not None and not payload.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")

    if payload.title is not None:
        task.title = payload.title.strip()
    if payload.done is not None:
        task.done = payload.done

    return task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    tasks.remove(task)
    return Response(status_code=204)


# ---------- Bonus: extras ----------

@app.get("/stats", summary="Task stats")
def stats():
    total = len(tasks)
    done = len([t for t in tasks if t.done])
    return {"total": total, "done": done, "open": total - done}


@app.post("/reset", response_model=List[Task], summary="Reset to example tasks")
def reset_tasks():
    global tasks, next_id
    tasks = [
        Task(id=1, title="Buy milk", done=False),
        Task(id=2, title="Write README", done=False),
        Task(id=3, title="Ship the API", done=True),
    ]
    next_id = 4
    return tasks
