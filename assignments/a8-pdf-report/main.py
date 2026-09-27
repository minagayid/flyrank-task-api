import uuid
from pathlib import Path
from fastapi import FastAPI,HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
app=FastAPI(title='PDF Report Generator'); OUT=Path(__file__).with_name('reports'); OUT.mkdir(exist_ok=True)
class ReportRequest(BaseModel): title:str='Task report'; total:int=0; done:int=0
@app.post('/reports',status_code=202)
def create(p:ReportRequest):
    rid=str(uuid.uuid4()); path=OUT/(rid+'.pdf'); c=canvas.Canvas(str(path),pagesize=LETTER); c.setTitle(p.title); c.drawString(72,720,p.title); c.drawString(72,690,f'Total tasks: {p.total}'); c.drawString(72,670,f'Completed tasks: {p.done}'); c.drawString(72,650,f'Open tasks: {p.total-p.done}'); c.save(); return {'id':rid,'status':'complete','download_url':f'/reports/{rid}/download'}
@app.get('/reports/{rid}/download')
def download(rid:str):
    path=OUT/(rid+'.pdf')
    if not path.exists(): raise HTTPException(404,detail='Report not found')
    return FileResponse(path,media_type='application/pdf',filename='task-report.pdf')
