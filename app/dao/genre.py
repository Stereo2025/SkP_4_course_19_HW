from app.dao.model.genre import Genre


class GenreDAO:
    """CRUD для таблицы genre"""

    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        """Получает жанр по id"""

        return self.session.query(Genre).get(bid)

    def get_all(self):
        """Получает все жанры"""

        return self.session.query(Genre).all()

    def create(self, genre_d):
        """Создает новый жанр в БД"""

        ent = Genre(**genre_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, genre_d):
        """Обновляет жанр"""

        genre = self.get_one(genre_d.get("id"))
        genre.name = genre_d.get("name")

        self.session.add(genre)
        self.session.commit()

    def delete(self, rid):
        """Удаляет жанр по id"""

        genre = self.get_one(rid)
        self.session.delete(genre)
        self.session.commit()
#######################################################################################################################
