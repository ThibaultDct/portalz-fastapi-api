from functools import lru_cache
import logging
import random
import string
import time
from urllib.request import Request
from supabase import create_client, Client
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import config as config
import bcrypt as bcrypt
from app.db import models as models

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()

@lru_cache()
def get_settings():
    return config.Settings()

supabase: Client = create_client(get_settings().supabase_url, get_settings().supabase_key)
salt: str = get_settings().salt

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response


@app.get("/")
async def root():
    logger.info("logging from the root logger")
    return {"status": "alive"}

@app.get("/users")
def users():
    users = supabase.table('users').select('*').execute()
    return users

@app.post("/users")
def new_user(user: models.UserDto):
    hashed_password = user.password.encode('utf-8')
    new_user = models.User(username = user.username, password = bcrypt.hashpw(hashed_password, bcrypt.gensalt()), email = user.email)
    supabase.table('users').insert(jsonable_encoder(new_user)).execute()