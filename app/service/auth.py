import calendar
import jwt
from flask_restx import abort
import datetime
from app.helpers.constants import JWT_SECRET, JWT_ALGORITHM
from app.service.user import UserService


class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        """
        Получив username и password находит нужного пользователя.
        Если такого пользователя нет, то 404.
        При успешном нахождении пользователя, вызывается compare_passwords,
        в неё передаётся пароль - 'хэш' у найденного пользователя и сам пароль 'строку'.
        Если они не равны отдаём 400, если равны, формируется словарь data,
        затем access_token и refresh_token.
        """

        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            'username': user.username,
            'role': user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        days30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data['exp'] = calendar.timegm(days30.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        """
         Декодирует токен с помощью ключа и алгоритма, таким образом получая инфо о пользователе.
         Извлекает имя пользователя, и т.к. здесь именно refresh_token, пароль у юзера заново
         не запрашивается.
        """

        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = data.get('username')
        return self.generate_tokens(username, None, is_refresh=True)
#######################################################################################################################
