from flask import request
from flask_restx import Resource, Namespace
from app.dao.model.director import DirectorSchema
from app.helpers.decorators import auth_required, admin_required
from app.implemented import director_service


director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):

    @auth_required
    def get(self):
        """Получение БД по всем режисерам привелегия авторизованного юзера"""

        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        """Добавление в БД режисера привелегия админа"""

        query = request.json
        director = director_service.create(query)
        return '', 201, {"location": f"/directors/{director.id}"}


@director_ns.route('/<int:rid>')
class DirectorView(Resource):

    @auth_required
    def get(self, rid):
        """Получение данных по режисерам из БД по id привелегия авторизованного юзера"""

        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        """Обновление данных в БД привелегия админа"""

        query = request.json
        if 'id' not in query:
            query['id'] = rid
        director_service.update(query)
        return '', 204

    @admin_required
    def delete(self, rid):
        """Удаление данных из БД привелегия админа"""

        director_service.delete(rid)
        return '', 204
#######################################################################################################################
