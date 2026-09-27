import time,uuid
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app=FastAPI(title='Background Job API'); jobs={}; pool=ThreadPoolExecutor(max_workers=2)
class JobIn(BaseModel): text:str

def work(jid,text):
    j=jobs[jid]; j['status']='running'; j['attempts']+=1
    try: time.sleep(.05); j.update(status='complete',result={'length':len(text),'uppercase':text.upper()})
    except Exception as e: j.update(status='failed',error=str(e))
@app.post('/jobs',status_code=202)
def enqueue(p:JobIn):
    jid=str(uuid.uuid4()); jobs[jid]={'id':jid,'status':'queued','attempts':0}; pool.submit(work,jid,p.text); return jobs[jid]
@app.get('/jobs/{jid}')
def status(jid:str):
    if jid not in jobs: raise HTTPException(404,detail='Job not found')
    return jobs[jid]
@app.post('/jobs/{jid}/retry',status_code=202)
def retry(jid:str):
    if jid not in jobs: raise HTTPException(404,detail='Job not found')
    jobs[jid]['status']='queued'; pool.submit(work,jid,'retry'); return jobs[jid]
