from fastapi.testclient import TestClient
from main import app
c=TestClient(app)
def test_eight_cases():
    for text in ['urgent outage','ASAP please','security issue','normal update','hello','question','follow up','routine task']:
        r=c.post('/judge',json={'text':text}); assert r.status_code==200; assert 0<=r.json()['confidence']<=1
