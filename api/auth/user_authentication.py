"""
Authentication module for JWT token
"""
import datetime

import bcrypt
import jwt
from flask import current_app

from api.models.objects.user import UserModel
from api.models.users_model import Users
from api.utils.singleton import Singleton


class Authenticate(metaclass=Singleton):
    """Defines methods used by JWT token"""

    __users = Users()

    @classmethod
    def authenticate_handler(cls, username, password):
        """
        jwt method handler to verify user token
        :param username:
        :param password:
        :return:
        """
        user = cls.__users.find_user_by_contact(username)
        if user and Authenticate.verify_password(password, user.password):
            return user

    @classmethod
    def identity_handler(cls, payload) -> UserModel:
        """
        jwt method to retrieve user identity/ID
        :param payload:
        :return:
        """
        if not isinstance(payload, str):
            user_id = payload['user_id']
            user = cls.__users.find_user_by_id(user_id)
            if user:
                return user

    @staticmethod
    def encode_auth_token(user: UserModel):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=60),
                'iat': datetime.datetime.utcnow(),
                'sub': user.__dict__,
                'identity': user.user_id,
            }
            return jwt.encode(payload, current_app.config.get('SECRET_KEY'),
                              algorithm='HS256')
        except Exception as ex:
            print(ex)
            return ex

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def hash_password(password):
        """
        method to hash password with bcrypt
        :param password:
        :return:
        """
        try:
            return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt(12))
        except ValueError:
            return False

    @staticmethod
    def verify_password(text, hashed):
        """
        verify client password with stored password
        :param text:
        :param hashed:
        :return:
        """
        try:
            return bcrypt.checkpw(text.encode("utf8"), hashed)
        except ValueError:
            return False
