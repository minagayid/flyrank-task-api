from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, model_validator

app = FastAPI(title="Task API", version="1.0", description="A small in-memory CRUD API.")


class Task(BaseModel):
    id: int
    title: str
    done: bool


class CreateTask(BaseModel):
    title: str = Field(..., description="Task title")

    @model_validator(mode="after")
    def title_must_not_be_empty(self):
        if not self.title.strip():
            raise ValueError("title must not be empty")
        return self


class UpdateTask(BaseModel):
    title: Optional[str] = Field(None, description="Replacement task title")
    done: Optional[bool] = Field(None, description="Whether the task is complete")

    @model_validator(mode="after")
    def update_must_have_valid_values(self):
        if self.title is None and self.done is None:
            raise ValueError("provide title or done")
        if self.title is not None and not self.title.strip():
            raise ValueError("title must not be empty")
        return self


# Deliberately in memory: data resets when the server restarts.
tasks = [
    Task(id=1, title="Learn HTTP basics", done=True),
    Task(id=2, title="Build a CRUD API", done=False),
    Task(id=3, title="Test with Swagger UI", done=False),
]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"error": "Invalid request: " + "; ".join(error["msg"] for error in exc.errors())})


@app.get("/", summary="Describe the API")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Check server health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task], summary="List all tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task, summary="Get one task")
def get_task(task_id: int):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, summary="Create a task")
def create_task(payload: CreateTask):
    next_id = max((task.id for task in tasks), default=0) + 1
    task = Task(id=next_id, title=payload.title.strip(), done=False)
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task, summary="Update a task")
def update_task(task_id: int, payload: UpdateTask):
    task = next((task for task in tasks if task.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    if payload.title is not None:
        task.title = payload.title.strip()
    if payload.done is not None:
        task.done = payload.done
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return None
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
