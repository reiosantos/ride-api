"""User module to handle user actions like creation"""
from typing import List

from api.config.database import DatabaseConnection
from api.utils.utils import JSONSerializable, Utils


class Users:
    """Define user module attributes accessed by callers """

    __table = "users"
    __database = DatabaseConnection.connect()

    class UserModel(JSONSerializable):
        """ User modal to hold user data"""

        def __init__(self, full_name=None, contact=None, username=None,
                     password=None, user_type=None):
            """
            user modal template
            :param full_name:
            :param contact:
            :param username:
            :param password:
            :param user_type:
            """
            self.user_id = Utils.generate_user_id()
            self.registration_date = Utils.make_date_time()

            self.full_name = full_name
            self.username = username
            self.contact = contact
            self.password = password
            self.user_type = user_type

        def __str__(self):
            return "User(id='%s')" % self.user_id

    @classmethod
    def create_user(cls, full_name=None, contact=None, username=None,
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

        user = Users.UserModel(full_name, contact, username, password, user_type)
        data = {
            "username": username,
            "full_names": full_name,
            "contact": contact,
            "password": password.decode("utf8"),
            "user_type": user_type,
            "registration_date": user.registration_date,
            "user_id": user.user_id
        }
        ret = cls.__database.insert(cls.__table, data)
        if not ret:
            return None

        return user

    @classmethod
    def find_user_by_id(cls, user_id) -> UserModel or bool:
        """
        Find a specific user given an id
        :param user_id:
        :return:
        """
        criteria = {
            "user_id": user_id
        }
        res = cls.__database.find(cls.__table, criteria=criteria)
        if res and isinstance(res, dict):
            user = cls.UserModel(res['full_names'], res['contact'], res['username'],
                                 None, res['user_type'])
            user.user_id = res['user_id']
            user.password = res['password'].encode("utf8")
            return user
        return False

    @classmethod
    def find_user_by_contact(cls, contact) -> UserModel or None:
        """
        Find a specific user given an id
        :param contact:
        :return:
        """

        criteria = {
            "contact": contact
        }
        res = cls.__database.find(cls.__table, criteria=criteria)
        if res and isinstance(res, dict):
            user = cls.UserModel(res['full_names'], res['contact'], res['username'],
                                 None, res['user_type'])
            user.user_id = res['user_id']
            user.password = res['password'].encode("utf8")
            return user
        return None

    @classmethod
    def find_user_by_username(cls, username) -> UserModel or None:
        """
        Find a specific user given an id
        :param username:
        :return:
        """

        criteria = {
            "username": username
        }
        res = cls.__database.find(cls.__table, criteria=criteria)
        if res and isinstance(res, dict):
            user = cls.UserModel(res['full_names'], res['contact'], res['username'],
                                 None, res['user_type'])
            user.user_id = res['user_id']
            user.password = res['password'].encode("utf8")
            return user
        return None

    @classmethod
    def get_all_users(cls) -> List[UserModel] or None:
        """
        Fetch a list of all users
        :return:
        """
        response = cls.__database.find(cls.__table)
        if response and isinstance(response, list):
            us: List[cls.UserModel] = []
            for res in response:
                user = cls.UserModel(res['full_names'], res['contact'], res['username'],
                                     None, res['user_type'])
                user.user_id = res['user_id']
                user.password = res['password'].encode("utf8")
                us.append(user)
            return us
        return None

    @classmethod
    def update_user(cls, user_id=None, full_name=None, contact=None, username=None,
                    password=None, user_type="passenger") -> bool:
        """
        Update user profile
        :param user_id:
        :param full_name:
        :param contact:
        :param username:
        :param password:
        :param user_type:
        :return:
        """

        user = cls.find_user_by_id(user_id)
        if not user:
            return False

        selection = {
            "user_id": user_id,
        }
        data = {
            "full_names": full_name or user.full_name,
            "contact": contact or user.contact,
            "username": username or user.username,
            "user_type": user_type or user.user_type,
            "password": password or user.password
        }
        return cls.__database.update(cls.__table, selection, data)

    @classmethod
    def delete_user(cls, user_id) -> bool:
        """
        delete a particular user
        :param user_id:
        :return:
        """

        user = cls.find_user_by_id(user_id)
        if not user:
            return False

        selection = {
            "user_id": user_id,
        }
        return cls.__database.delete(cls.__table, selection)
