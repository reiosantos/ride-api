"""User module to handle user actions like creation"""
from typing import List

from api.utils.utils import JSONSerializable, Utils


class Users:
    """Define user module attributes accessed by callers """

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

    users: List[UserModel] = []

    @staticmethod
    def create_user(full_name=None, contact=None, username=None,
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
        Users.users.append(user)
        return user

    @classmethod
    def get_all_users(cls) -> List[UserModel]:
        """
        Fetch a list of all users
        :return:
        """
        return cls.users

    @classmethod
    def find_user_by_id(cls, user_id) -> UserModel or bool:
        """
        Find a specific user given an id
        :param user_id:
        :return:
        """

        for user in cls.users:
            if user.user_id == user_id:
                return user
        return False

    @classmethod
    def find_user_by_contact(cls, contact) -> UserModel or None:
        """
        Find a specific user given an id
        :param contact:
        :return:
        """

        for user in cls.users:
            if user.contact == contact:
                return user
        return None

    @classmethod
    def find_user_by_username(cls, username) -> UserModel or None:
        """
        Find a specific user given an id
        :param username:
        :return:
        """

        for user in cls.users:
            if user.username == username:
                return user
        return Users.find_user_by_contact(contact=username)

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
        index = cls.users.index(user)

        user.user_type = user_type
        if password:
            user.password = password
        user.full_name = full_name
        user.contact = contact
        user.username = username

        cls.users.insert(index, user)
        return True

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

        cls.users.remove(user)
        return True
