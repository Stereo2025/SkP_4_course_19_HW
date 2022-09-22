from flask import request
from flask_restx import Resource, Namespace
from app.dao.model.genre import GenreSchema
from app.helpers.decorators import auth_required, admin_required
from app.implemented import genre_service


genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):

    @auth_required  # Авторизированные пользователи
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required  # Только админ
    def post(self):
        query = request.json
        genre = genre_service.create(query)
        return '', 201, {"location": f"/genres/{genre.id}"}


@genre_ns.route('/<int:rid>')
class GenreView(Resource):

    @auth_required  # Авторизированные пользователи
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required  # Только админ
    def put(self, rid):
        query = request.json
        if 'id' not in query:
            query['id'] = rid
        genre_service.update(query)
        return '', 204

    @admin_required  # Только админ
    def delete(self, rid):
        genre_service.delete(rid)
        return '', 204
#######################################################################################################################
