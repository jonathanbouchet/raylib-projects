from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()


# Data Model (Schema)
class ToDo(BaseModel):
    id: int
    title: str


class ToDoUser(BaseModel):
    title: str


# In-memory database
# db = []
db = [{"id": 0, "title": "TEST1"}, {"id":1, "title": "TEST2"}]


# Health
@app.get("/")
def root() -> dict[str, str]:
    return {"status": "api ok"}


# CREATE: Add a new todo
@app.post("/todos/", response_model=ToDo)
def create_todo(todo: ToDoUser):
    db_size: int = len(db)
    todo_to_insert = ToDo(id=db_size, title=todo.title)
    db.append(todo_to_insert)
    return todo_to_insert


# READ: Get all todos or a specific one
@app.get("/todos/", response_model=List[ToDo])
def read_todos():
    return db


@app.get("/todos/{todo_id}", response_model=ToDo)
def read_todo(todo_id: int):
    for todo in db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="todo not found")


# UPDATE: Modify an existing todo
@app.put("/todos/{todo_id}", response_model=ToDo)
def update_todo(todo_id: int, updated_todo: ToDo):
    for index, todo in enumerate(db):
        if todo.id == todo_id:
            db[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="todo not found")


# DELETE: Remove an todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(db):
        if todo.id == todo_id:
            db.pop(index)
            return {"message": "ToDO deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ToDo not found")
