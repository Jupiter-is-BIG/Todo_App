from fastapi import FastAPI, Depends, HTTPException
from models import todo_model, single_todo_model
from utils.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

app = FastAPI()

todo_model.Base.metadata.create_all(bind = engine)

@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(todo_model.Todos).all()

@app.post("/")
async def create_todo( new_todo: single_todo_model.SingleTodo, db: Session = Depends(get_db)):
    todo = todo_model.Todos()
    todo.title = new_todo.title
    todo.description = new_todo.description
    todo.priority = new_todo.priority
    todo.completed = new_todo.completed
    db.add(todo)
    db.commit()
    
    return {
        'status': 201,
        'description': 'Todo added!'
    }
    

@app.get("/todo/{todo_id}")
async def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
):
    query = db.query(todo_model.Todos).filter(todo_model.Todos.id == todo_id).first()
    if query:
        return query
    raise HTTPException(status_code=404, detail="Todo Not Found")

@app.put("/{todo_id}")
async def update_todo(
    todo_id: int,
    new_todo: single_todo_model.SingleTodo,
    db: Session = Depends(get_db),
):
    query = db.query(todo_model.Todos).filter(todo_model.Todos.id == todo_id).first()
    if query:
        query.title = new_todo.title
        query.description = new_todo.description
        query.priority = new_todo.priority
        query.completed = new_todo.completed

        db.add(query)
        db.commit()

        return {
        'status': 200,
        'description': 'Todo updated!'
        }

    raise HTTPException(status_code=404, detail="Todo Not Found")

@app.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
):
    query = db.query(todo_model.Todos).filter(todo_model.Todos.id == todo_id).first()

    if query:
        db.delete(query)
        db.commit()
        return {
            'status': 200,
            'description': 'Todo deleted!'
        }
        
    raise HTTPException(status_code=404, detail="Todo Not Found")
