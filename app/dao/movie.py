from app.dao.model.movie import Movie


class MovieDAO:
    """CRUD для таблицы movie"""

    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        """Получает фильм по id"""

        return self.session.query(Movie).get(bid)

    def get_all(self):
        """Получает все фильмы"""

        return self.session.query(Movie).all()

    def get_by_director_id(self, val):
        """Получает фильмы по id режисера"""

        return self.session.query(Movie).filter(Movie.director_id == val).all()

    def get_by_genre_id(self, val):
        """Получает фильмы по id жанра"""

        return self.session.query(Movie).filter(Movie.genre_id == val).all()

    def get_by_year(self, val):
        """Получает фильмы по году"""

        return self.session.query(Movie).filter(Movie.year == val).all()

    def create(self, movie_d):
        """Создаёт новый фильм в БД"""

        ent = Movie(**movie_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, movie_d):
        """Обновляет фильмы"""

        movie = self.get_one(movie_d.get("id"))
        movie.title = movie_d.get("title")
        movie.description = movie_d.get("description")
        movie.trailer = movie_d.get("trailer")
        movie.year = movie_d.get("year")
        movie.rating = movie_d.get("rating")
        movie.genre_id = movie_d.get("genre_id")
        movie.director_id = movie_d.get("director_id")

        self.session.add(movie)
        self.session.commit()

    def delete(self, rid):
        """Удаляет фильм из БД по id"""

        movie = self.get_one(rid)
        self.session.delete(movie)
        self.session.commit()
#######################################################################################################################
