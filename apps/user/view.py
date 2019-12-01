from datetime import timedelta, datetime

import jwt
from fastapi import Form
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
import pandas as pd
from apps.user import router
from apps.user.models import USER
from apps.user.sql_models import User
from system_item.setting import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from utils.aiopg_conf import database
from passlib.hash import django_pbkdf2_sha256


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")





def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


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
    print(encoded_jwt)
    return encoded_jwt


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    # 返回当前用户
    return current_user

@router.post('/authorizations/')
async def demo(username:str=Form(...),password:str=Form(...)):
    """
    用户登录
    1 判断用户名是否存在，存在则拿出密码
    2 对密码加密，再对比数据库的数据
    3 正确返回生成的token
    :param username:
    :param password:
    :return:
    """
    # 获取用户
    user_query = select([User.c.username,User.c.password]).where(User.c.username==username)
    user = await  database.fetch_one(user_query)
    if not user:
        return '1'
    me = USER(**user)
    is_true = verify_pw(password,me.password)
    if not is_true:
        return '2'
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": me.username}, expires_delta=access_token_expires
    ).decode()
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    print(username)
    data = {
        "code": 0,
        "message": {"token": access_token,
                    "time": 86300
                    }

    }
    return data
    # 密码加密
