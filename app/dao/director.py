from app.dao.model.director import Director


class DirectorDAO:
    """CRUD для таблицы director"""

    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        """Получает режисера по его id"""

        return self.session.query(Director).get(bid)

    def get_all(self):
        """Получает всех режисеров"""

        return self.session.query(Director).all()

    def create(self, director_d):
        """Создаёт нового режисера в БД"""

        ent = Director(**director_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, director_d):
        """Обновляет данные режисера"""

        director = self.get_one(director_d.get("id"))
        director.name = director_d.get("name")

        self.session.add(director)
        self.session.commit()

    def delete(self, rid):
        """Удаляет режисера по id"""

        director = self.get_one(rid)
        self.session.delete(director)
        self.session.commit()
#######################################################################################################################
