from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

tasks: Dict[int, dict] = {}
task_id_counter = 1

class Task(BaseModel):
    title: str
    description: str = ""

@app.post("/tasks/")
def create_task(task: Task):
    global task_id_counter
    tasks[task_id_counter] = {"title": task.title, "description": task.description}
    task_id_counter += 1
    return {"id": task_id_counter - 1, "task": tasks[task_id_counter - 1]}

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id, "task": tasks[task_id]}

@app.get("/tasks/")
def read_all_tasks():
    return tasks

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = {"title": task.title, "description": task.description}
    return {"id": task_id, "task": tasks[task_id]}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"detail": "Task deleted"}
