import base64
import hashlib
import hmac

from app.dao.user import UserDAO
from app.helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:

    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_by_username(self, uid):
        return self.dao.get_by_username(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        """Перезаписывает поле password которое передаётся при POST запросе"""

        user_d['password'] = self.generate_password(user_d['password'])
        return self.dao.create(user_d)

    def update(self, user_d):
        """Перезаписывает поле password которое передаётся при PUT запросе"""

        user_d['password'] = self.generate_password(user_d['password'])
        self.dao.update(user_d)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def generate_password(self, password) -> bytes:
        """
        На основании выбранного алгоритма и какой-то строки,
        создаёт бинарную последовательность чисел,
        которые мы можем использовать как пароль.
        """

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def compare_passwords(self, password_hash, other_password) -> bool:
        """
        Декодирует password_hash из base64 в бинарное представление.
        Вызывает через hmac - compare_digest который сравнивает эти два
        бинарных представления, и затем выдаёт True или False.
        """

        decode_digest = base64.b64decode(password_hash)
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decode_digest, hash_digest)
#######################################################################################################################
