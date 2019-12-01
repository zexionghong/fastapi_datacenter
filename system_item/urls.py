from apps import  user
from main import app



app.include_router(router=user.router)    #用户模块
