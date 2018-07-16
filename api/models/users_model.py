"""User module to handle user actions like creation"""

from api.config.database import DatabaseConnection
from api.models.objects.user import UserModel
from api.utils.singleton import Singleton
from api.utils.utils import Utils


class Users(metaclass=Singleton):
    """Define user module attributes accessed by callers """

    __table = "users"
    __database = DatabaseConnection()

    def create_user(self, full_name=None, contact=None, username=None,
                    password=None, user_type="passenger") -> UserModel or None:
        """
        create new user withe details below
        :param full_name:
        :param contact:
        :param username:
        :param password:
        :param user_type:
        :return:
        """

        user = UserModel(full_name, contact, username, password, user_type)
        data = {
            "username": username,
            "full_names": full_name,
            "contact": contact,
            "password": password.decode("utf8"),
            "user_type": user_type,
            "registration_date": user.registration_date,
            "user_id": user.user_id
        }
        ret = self.__database.insert(self.__table, data)
        if not ret:
            return None

        return user

    def find_user_by_id(self, user_id) -> UserModel or bool:
        """
        Find a specific user given an id
        :param user_id:
        :return:
        """
        criteria = {
            "user_id": user_id
        }
        res = self.__database.find(self.__table, criteria=criteria)
        if res and isinstance(res, dict):
            user = UserModel(res['full_names'], res['contact'], res['username'],
                             None, res['user_type'])
            user.user_id = res['user_id']
            user.password = res['password'].encode("utf8")
            return user
        return False

    def find_user_by_contact(self, contact) -> UserModel or None:
        """
        Find a specific user given an id
        :param contact:
        :return:
        """

        criteria = {
            "contact": contact
        }
        res = self.__database.find(self.__table, criteria=criteria)
        if res and isinstance(res, dict):
            user = UserModel(res['full_names'], res['contact'], res['username'],
                             None, res['user_type'])
            user.user_id = res['user_id']
            user.password = res['password'].encode("utf8")
            return user
        return None

    def find_user_by_username(self, username) -> UserModel or None:
        """
        Find a specific user given an id
        :param username:
        :return:
        """

        criteria = {
            "username": username
        }
        res = self.__database.find(self.__table, criteria=criteria)
        if res and isinstance(res, dict):
            user = UserModel(res['full_names'], res['contact'], res['username'],
                             None, res['user_type'])
            user.user_id = res['user_id']
            user.password = res['password'].encode("utf8")
            return user
        return self.find_user_by_contact(username)

    def update_last_login(self, username, contact):
        """
        update user last login date
        :param username:
        :return:
        """
        criteria = {
            "username": username,
            "contact": contact
        }
        data = {
            "last_login": Utils.make_date_time(),
        }
        self.__database.update(self.__table, criteria, data)
