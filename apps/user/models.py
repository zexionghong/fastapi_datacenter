import datetime

from pydantic import BaseModel


class USER(BaseModel):
    id: int = None
    group_id:int= None
    username:str= None
    realname:str= None
    password:str= None
    salt:str= None
    status:int= None
    create_time: datetime.datetime= None
    update_time:datetime.datetime= None
    last_login_time:datetime.datetime= None
    level:int= None
    email:str= None
    mobile:int= None
    company:str= None
    department_id:int= None
    is_del:int= None

class USERS(BaseModel):
    user:list = USER


