"""
Task Manager - FastAPI Application
Simple REST API for managing tasks with a web interface
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Task Manager", description="A simple task management API", version="1.0.0")

# In-memory storage for tasks
# NOTE: This simple implementation is not thread-safe and suitable for demo/development only.
# For production use, consider using a database and proper concurrency handling.
tasks_db = []
task_id_counter = 1


class Task(BaseModel):
    """Task model"""
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[str] = None


class TaskCreate(BaseModel):
    """Task creation model"""
    title: str
    description: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint - redirect to static interface"""
    with open("static/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.get("/api/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks"""
    return tasks_db


@app.post("/api/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task"""
    global task_id_counter
    
    new_task = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        completed=False,
        created_at=datetime.now().isoformat()
    )
    
    tasks_db.append(new_task.model_dump())
    task_id_counter += 1
    
    return new_task


@app.get("/api/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Get a specific task by ID"""
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/api/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: Task):
    """Update a task"""
    for idx, task in enumerate(tasks_db):
        if task["id"] == task_id:
            task_update.id = task_id
            task_update.created_at = task["created_at"]
            tasks_db[idx] = task_update.model_dump()
            return task_update
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task"""
    for idx, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(idx)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
