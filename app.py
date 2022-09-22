from flask import Flask
from flask_restx import Api

from app.config import Config
from app.setup_db import db
from app.views.directors import director_ns
from app.views.genres import genre_ns
from app.views.movies import movie_ns
from app.views.users import users_ns
from app.views.auth import auth_ns


def create_app(config_object: Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.app_context().push()
    return app


def configure_app(app: Flask):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(users_ns)
    api.add_namespace(auth_ns)


def create_data():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    configure_app(app)
    create_data()
    app.run()
#######################################################################################################################
