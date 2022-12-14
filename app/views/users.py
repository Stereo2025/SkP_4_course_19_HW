from flask import request
from flask_restx import Resource, Namespace
from app.dao.model.user import UserSchema
from app.helpers.decorators import admin_required
from app.implemented import user_service


users_ns = Namespace('users')


@users_ns.route('/')
class UsersView(Resource):

    @admin_required
    def get(self):
        """Получение данных из БД по юзеру привелегия админа"""

        user = user_service.get_all()
        result = UserSchema(many=True).dump(user)
        return result, 200

    def post(self):
        """Зарегестрироваться может любой юзер"""

        query = request.json
        user = user_service.create(query)
        return f'User {user.username} is added', 201, {"location": f"/users/{user.id}"}


@users_ns.route('/<int:uid>')
class UserView(Resource):

    @admin_required
    def get(self, uid):
        """Получение данных из БД по юзеру привелегия админа"""

        user = user_service.get_one(uid)
        result = UserSchema().dump(user)
        return result, 200

    @admin_required
    def put(self, uid):
        """Обновление данных в БД привелегия админа"""

        query = request.json
        if 'id' not in query:
            query['id'] = uid
        user_service.update(query)
        return '', 204

    @admin_required
    def delete(self, uid):
        """Удаление данных из БД привелегия админа"""

        user_service.delete(uid)
        return '', 204
#######################################################################################################################
