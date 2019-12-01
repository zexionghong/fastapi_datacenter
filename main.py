import time
from typing import List

import jwt
from fastapi import FastAPI
from fastapi.params import Header
from sqlalchemy import select
from starlette.requests import Request

from apps import user
from system_item.setting import SECRET_KEY, ALGORITHM
from utils.aiopg_conf import database

app = FastAPI()
app.include_router(router=user.router)



@app.middleware("http")
async def add_process_time_header(request: Request, call_next,Authorization: str = Header(None)):
    start_time = time.time()
    print('请求前')
    print(request.headers.get('authorization'))
    # 解析用户
    request.scope['user'] = '1111'
    response = await call_next(request)
    print('请求后')
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/items/")
async def read_items(*, request:Request):
    Authorization = request.headers.get('Authorization').split(' ')[-1]
    print(Authorization)
    payload = jwt.decode(Authorization, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    print(username)
    print(request.user)

    print('请求中')
    return {"Authorization": Authorization}