import os, psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app=FastAPI(title='Task API - Postgres')
class TaskIn(BaseModel): title:str; done:bool=False
def conn(): return psycopg.connect(os.getenv('DATABASE_URL','postgresql://tasks:tasks@db:5432/tasks'), row_factory=dict_row)
def init():
    with conn() as c:
        c.execute('CREATE TABLE IF NOT EXISTS tasks(id SERIAL PRIMARY KEY,title TEXT NOT NULL,done BOOLEAN NOT NULL DEFAULT FALSE)')
        if c.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]==0: c.executemany('INSERT INTO tasks(title,done) VALUES(%s,%s)',[('Docker persistence',True),('Use a volume',False),('Keep routes stable',False)])
@app.on_event('startup')
def startup(): init()
@app.get('/tasks')
def all():
    with conn() as c: return [dict(r) for r in c.execute('SELECT id,title,done FROM tasks ORDER BY id').fetchall()]
@app.get('/tasks/{id}')
def one(id:int):
    with conn() as c: r=c.execute('SELECT id,title,done FROM tasks WHERE id=%s',(id,)).fetchone()
    if not r: raise HTTPException(404,detail=f'Task {id} not found')
    return dict(r)
@app.post('/tasks',status_code=201)
def create(p:TaskIn):
    if not p.title.strip(): raise HTTPException(400,detail='title must not be empty')
    with conn() as c: r=c.execute('INSERT INTO tasks(title,done) VALUES(%s,%s) RETURNING id,title,done',(p.title.strip(),p.done)).fetchone()
    return dict(r)
