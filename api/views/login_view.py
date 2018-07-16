"""
Login user module
Allow user to login
"""
import copy

from flask import request, jsonify
from flask.views import MethodView

from api.auth.user_authentication import Authenticate
from api.errors.return_errors import ReturnError
from api.models.users_model import Users
from api.utils.decorators import Decorate


class LoginController(MethodView):
    """
    User Login Resource
    """
    __users = Users()

    @Decorate.receive_json
    def post(self):
        """
        login user and create jwt token
        :return:
        """
        # get the post data
        post_data = request.get_json()
        try:
            keys = ("username", "password")
            if not set(keys).issubset(set(post_data)):
                return ReturnError.missing_fields(keys)

            # fetch the user data
            user = self.__users.find_user_by_username(username=post_data.get('username'))
            if user:
                if not Authenticate.verify_password(post_data.get('password'), user.password):
                    return ReturnError.invalid_credentials()

                user = copy.deepcopy(user)
                del user.password
                auth_token = Authenticate.encode_auth_token(user)

                if auth_token:
                    self.__users.update_last_login(user.username, user.contact)
                    response_object = {
                        'data': False,
                        'user': user.__dict__,
                        'success_message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return jsonify(response_object), 200
            return ReturnError.user_not_found()

        except FileNotFoundError:
            response_object = {
                'data': False,
                'error_message': 'Try again'
            }
            return jsonify(response_object), 500
