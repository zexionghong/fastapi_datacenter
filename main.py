import time
import jwt
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.params import Header
from starlette.requests import Request
from starlette.responses import JSONResponse

from apps import user
from apps.user.models import USER
from system_item.setting import SECRET_KEY, ALGORITHM
from utils.aiopg_conf import jade_db
from utils.response_code import RET
from utils.utils import get_user


class NoDataErr(Exception):
    def __init__(self,name):
        self.name = name

app = FastAPI()
from system_item import  urls
# app.include_router(router=user.router)



@app.on_event("startup")
async def startup():
    """启动事件"""
    await jade_db.connect()


@app.on_event("shutdown")
async def startup():
    """启动事件"""
    await jade_db.disconnect()


@app.exception_handler(NoDataErr)
async def no_data_err(request: Request, exc: NoDataErr):
    return JSONResponse( status_code=404, content={'code':RET.NODATA,'message':'找不到该资源'})

#
@app.middleware("http")
async def add_process_time_header(request: Request, call_next,authorization: str = Header('authorization')):

    start_time = time.time()
    if request.url.path not in ('/test','/','/docs','/favicon.ico','/openapi.json','/authorizations/'):
        user = await get_user(request)
        if isinstance(user,JSONResponse):
            return user
        request.scope['user'] = user
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/test")
async def read_items(*, request:Request,authorization:str = Header(None)):
    print(request.headers)
    print(id(authorization))
    # Authorization = request.headers.get('Authorization').split(' ')[-1]
    # payload = jwt.decode(Authorization, SECRET_KEY, algorithms=[ALGORITHM])
    # username: str = payload.get("sub")
    #
    # print('请求中')
    # return {"Authorization": Authorization}


if __name__ == '__main__':

    uvicorn.run(app=app,host='0.0.0.0',port=8000,debug=True)