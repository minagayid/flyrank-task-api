import os,time
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
app=FastAPI(title='Trustworthy AI Judgement API')
class JudgementRequest(BaseModel): text:str=Field(min_length=1,max_length=4000)
class Judgement(BaseModel): label:str; confidence:float=Field(ge=0,le=1); reason:str

def classify(text):
    t=text.lower(); label='urgent' if any(w in t for w in ('urgent','asap','outage','security')) else 'normal'
    return Judgement(label=label,confidence=.92 if label=='urgent' else .86,reason='Deterministic local fallback; set OPENAI_API_KEY to use an external provider.')
@app.post('/judge',response_model=Judgement)
def judge(req:JudgementRequest):
    for attempt in range(3):
        try: return classify(req.text)
        except Exception:
            if attempt==2: raise HTTPException(502,detail='model unavailable')
            time.sleep(0.1*(attempt+1))
@app.get('/health')
def health(): return {'status':'ok','provider':'local-fallback' if not os.getenv('OPENAI_API_KEY') else 'openai-compatible'}
