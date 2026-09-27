import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
DB=Path(__file__).with_name('tasks.db'); app=FastAPI(title='Task API - SQLite')
class TaskIn(BaseModel):
    title:str
    @field_validator('title')
    @classmethod
    def nonempty(cls,v):
        if not v.strip(): raise ValueError('title must not be empty')
        return v.strip()
class Task(TaskIn): id:int; done:bool

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done BOOLEAN NOT NULL DEFAULT 0)')
    if c.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]==0:
        c.executemany('INSERT INTO tasks(title,done) VALUES(?,?)',[('Learn SQL',1),('Persist data',0),('Restart safely',0)])
    c.commit(); return c
def row(r): return {'id':r['id'],'title':r['title'],'done':bool(r['done'])}
@app.on_event('startup')
def startup(): db().close()
@app.get('/tasks')
def list_tasks():
    c=db(); out=[row(x) for x in c.execute('SELECT * FROM tasks ORDER BY id')]; c.close(); return out
@app.get('/tasks/{id}')
def get_task(id:int):
    c=db(); r=c.execute('SELECT * FROM tasks WHERE id=?',(id,)).fetchone(); c.close()
    if not r: raise HTTPException(404,detail=f'Task {id} not found')
    return row(r)
@app.post('/tasks',status_code=201)
def create(p:TaskIn):
    c=db(); cur=c.execute('INSERT INTO tasks(title,done) VALUES(?,0)',(p.title,)); c.commit(); r=c.execute('SELECT * FROM tasks WHERE id=?',(cur.lastrowid,)).fetchone(); c.close(); return row(r)
@app.put('/tasks/{id}')
def update(id:int,p:TaskIn|None=None,done:bool|None=None):
    c=db(); r=c.execute('SELECT * FROM tasks WHERE id=?',(id,)).fetchone()
    if not r: c.close(); raise HTTPException(404,detail=f'Task {id} not found')
    title=p.title if p else r['title']; c.execute('UPDATE tasks SET title=?,done=? WHERE id=?',(title,int(done if done is not None else r['done']),id)); c.commit(); r=c.execute('SELECT * FROM tasks WHERE id=?',(id,)).fetchone(); c.close(); return row(r)
@app.delete('/tasks/{id}',status_code=204)
def delete(id:int):
    c=db(); cur=c.execute('DELETE FROM tasks WHERE id=?',(id,)); c.commit(); c.close()
    if not cur.rowcount: raise HTTPException(404,detail=f'Task {id} not found')
