from datetime import timedelta, datetime
import jwt
from fastapi import Form
from fastapi.params import Depends, Header
from starlette.requests import Request
from apps.user import router
from system_item.setting import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from passlib.hash import django_pbkdf2_sha256
import pandas as pd
from utils.aiopg_conf import jade_db


def make_pw_hash(pw):
    # 密码加密，返回加密密码
    hash = django_pbkdf2_sha256.using(rounds=36000)
    hash_pw = hash.hash(pw)
    return hash_pw

def verify_pw(pw,db_pw):
    # 校验密码
    hash = django_pbkdf2_sha256.using(rounds=36000)
    is_true = hash.verify(pw,db_pw)
    return is_true

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    #创建一个jwt_token
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get('/user/center/?')
async def get_center_menu(request:Request,authorization:str = Header(None)):
    # 获取当前的用户
    user = request.scope.get('user')
    level = user.level
    if level ==0 :
        sql = '''select dm1.id pid,dm1.sort_id p_sort_id,dm1.menu_name p_name,dm2.id id,dm2.href,dm2.sort_id sort_id,dm2.menu_name  from data2_menu dm1 LEFT JOIN data2_menu dm2 on dm1.id=dm2.pid where dm1.pid = 0 '''.format(user.id)
    else:
        sql = '''
        select dm1.id pid,dm1.sort_id p_sort_id, dm1.menu_name p_name,dm2.id id,dm2.href,dm2.sort_id sort_id,dm2.menu_name  from data2_menu dm1 LEFT JOIN data2_menu dm2 on dm1.id=dm2.pid  RIGHT join data2_operator_auth da on da.menu_id=dm2.pid where dm1.pid = 0
        and group_id={}'''.format(user.group_id)
    data = await jade_db.fetch_all(sql)
    df = pd.DataFrame(data)
    data = []
    for p_menu in df.itertuples():
        tmp = {}
        data.append(tmp)
        tmp['yiji_menu'] = {
            'id': p_menu.pid,
            'name': p_menu.p_name,
            'href': '',
            'pid': 0,
            'osrt_id': p_menu.p_sort_id,
        }
        tmp['erji_menu'] = []
        for x, menu in df[df.pid == p_menu.pid].sort_values('sort').iterrows():
            dict_tmp = {
                'id': menu.id,
                'name': menu['name'],
                'href': menu.href,
                'pid': p_menu.pid,
                'sort_id': menu.sort
            }
            tmp['erji_menu'].append(dict_tmp)

    return {
        'code':"0",
        'message':data
    }


@router.get('/authorizations1/')
async def get_sign(request:Request):
    '''用户在登录状态下再次请求接口获取新 token来续签签字'''
    user = request.scope.get('user')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user.id, 'real_name': user.real_name, 'group_id': user.group_id,'level':user.level}, expires_delta=access_token_expires
    ).decode()
    data = {
        "code": 0,
        "message": {"token": access_token,
                    "time": 86300
                    }
    }
    return data


@router.post('/authorizations/')
async def demo(request:Request,username:str=Form(...),password:str=Form(...)):
    """
    :param username:
    :param password:
    :return:
    """
    # 获取用户
    # 判断是不是存在用户,判断密码加密后能否通过校验
    # 返回token
    print(id(request))
    data = await data_write_pool.fetch_one("select id,password,realname,group_id,level from data2_operator where username = '{username}' and is_del = 0 ; ".format(username=username))
    if not data:
        return "1"
    user_id,passworded,real_name,group_id,level = data

    is_true = verify_pw(password,passworded)
    if not is_true:
        return
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id":user_id,'real_name':real_name,'group_id':group_id,'level':level}, expires_delta=access_token_expires
    ).decode()

    data = {
        "code": 0,
        "message": {"token": access_token,
                    "time": 86300
                    }

    }
    return data
    # 密码加密
