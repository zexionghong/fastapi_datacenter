import jwt
from starlette.responses import JSONResponse
from apps.user.models import USER
from system_item.setting import SECRET_KEY, ALGORITHM

async def get_user(request):
    access_token = request.headers.get('authorization')
    if access_token:
        access_token = access_token.split()[-1]
    else:
        return JSONResponse('缺少token')
    try:
        payload = jwt.decode(bytes(access_token, encoding='utf-8'), SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return JSONResponse('用户信息错误')
    current_user = USER()

    current_user.group_id = payload.get('group_id')
    current_user.id = payload.get('id')
    current_user.real_name = payload.get('real_name')
    current_user.level = payload.get('level')
    return current_user


