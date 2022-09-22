import jwt
from flask import request, abort
from app.helpers.constants import JWT_SECRET, JWT_ALGORITHM


def auth_required(func):
    """
    Проверяет есть ли в заголовках нашего запроса есть Authorization. Если нет отдаёт 401.
    Если есть, извлекает токен, декодирует с помощью jwt.decode тем самым получая инфо о пользователе.
    """

    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except Exception as e:
            print('JWY Decode Exception', e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    """
    Проверка токена пользователя. Проверка роли юзера.
    Извлекает по ключу role значение из user. Если не задано, по умолчанию user.
    """

    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        role = None
        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user.get('role', 'user')
        except Exception as e:
            print('JWY Decode Exception', e)
            abort(401)

        if role != 'admin':
            abort(403)

        return func(*args, **kwargs)

    return wrapper
#######################################################################################################################
