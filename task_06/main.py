from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
from uuid import uuid4
from typing import Literal, List

app = FastAPI()

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr

class UserRead(BaseModel):
    id: str
    username: str
    email: EmailStr

class TaskBase(BaseModel):
    title: str
    description: str
    due_date: date

    @field_validator("due_date")
    def due_date_not_past(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("Due date cannot be in the past")
        return v

class TaskCreate(TaskBase):
    user_id: str

class Task(TaskBase):
    id: str
    status: Literal["pending", "in_progress", "done"]
    user_id: str

class TaskStatusUpdate(BaseModel):
    status: Literal["pending", "in_progress", "done"]

USERS: dict[str, UserRead] = {}
TASKS: dict[str, Task] = {}

@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    user_id = str(uuid4())
    user_obj = UserRead(id=user_id, **user.dict())
    USERS[user_id] = user_obj
    return user_obj

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: str):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    return USERS[user_id]

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    if task.user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    task_id = str(uuid4())
    new_task = Task(id=task_id, status="pending", **task.dict())
    TASKS[task_id] = new_task
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")
    return TASKS[task_id]

@app.put("/tasks/{task_id}", response_model=Task)
def update_task_status(task_id: str, status_update: TaskStatusUpdate):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")
    TASKS[task_id].status = status_update.status
    return TASKS[task_id]

@app.get("/users/{user_id}/tasks", response_model=List[Task])
def get_user_tasks(user_id: str):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    return [task for task in TASKS.values() if task.user_id == user_id]