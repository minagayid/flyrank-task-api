import os
from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
try:
 from supabase import create_client
 client=create_client(os.environ['SUPABASE_URL'],os.environ['SUPABASE_KEY']) if os.getenv('SUPABASE_URL') else None
except Exception: client=None
app=FastAPI(title='Secure Auth API')
class Credentials(BaseModel): email:str; password:str
def token(auth=Header(None)):
    if not auth or not auth.startswith('Bearer ') or not auth[7:]: raise HTTPException(401,detail='Access token required')
    if not client: raise HTTPException(503,detail='Supabase credentials are not configured')
    try: return client.auth.get_user(auth[7:]).user
    except Exception: raise HTTPException(401,detail='Invalid or expired token')
@app.post('/auth/signup',status_code=201)
def signup(p:Credentials):
    if not p.email or not p.password: raise HTTPException(400,detail='email and password are required')
    if not client: raise HTTPException(503,detail='Supabase credentials are not configured')
    try: return client.auth.sign_up({'email':p.email,'password':p.password}).user
    except Exception as e: raise HTTPException(400,detail=str(e))
@app.post('/auth/login')
def login(p:Credentials):
    if not p.email or not p.password: raise HTTPException(400,detail='email and password are required')
    if not client: raise HTTPException(503,detail='Supabase credentials are not configured')
    try:
        s=client.auth.sign_in_with_password({'email':p.email,'password':p.password}); return {'access_token':s.session.access_token,'refresh_token':s.session.refresh_token}
    except Exception: raise HTTPException(401,detail='Invalid login credentials')
@app.get('/public/info')
def public(): return {'message':'Welcome stranger! This info is public.'}
@app.get('/protected/profile')
def profile(user=Depends(token)): return {'id':user.id,'email':user.email,'created_at':user.created_at}
@app.get('/protected/dashboard')
def dashboard(user=Depends(token)): return {'message':'Protected dashboard','user_id':user.id}
@app.post('/auth/logout',status_code=204)
def logout(user=Depends(token)): client.auth.sign_out(); return None
