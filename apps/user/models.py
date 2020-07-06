import datetime

from pydantic import BaseModel


class USER(BaseModel):
    id: int = None
    group_id:int= None
    real_name:str= None
    department_id:int= None
    level:int= None

class USERS(BaseModel):
    user:list = USER


