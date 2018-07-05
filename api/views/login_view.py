"""
Login user module
Allow user to login
"""
import copy

from flask import request, jsonify
from flask.views import MethodView

from api.auth.user_authentication import Authenticate
from api.errors.return_errors import ReturnErrors
from api.models.users_model import Users
from api.utils.decorators import Decorate


class LoginController(MethodView):
    """
    User Login Resource
    """

    @staticmethod
    @Decorate.receive_json
    def post():
        """
        login user and create jwt token
        :return:
        """
        # get the post data
        post_data = request.get_json()
        try:
            keys = ("username", "password")
            if not set(keys).issubset(set(post_data)):
                return ReturnErrors.missing_fields(keys)

            # fetch the user data
            user = Users.find_user_by_username(username=post_data.get('username'))
            if user:
                if not Authenticate.verify_password(post_data.get('password'), user.password):
                    return ReturnErrors.invalid_credentials()

                user = copy.deepcopy(user)
                del user.password
                auth_token = Authenticate.encode_auth_token(user)
                if auth_token:
                    response_object = {
                        'data': False,
                        'success_message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return jsonify(response_object), 200
            return ReturnErrors.user_not_found()

        except FileNotFoundError:
            response_object = {
                'data': False,
                'error_message': 'Try again'
            }
            return jsonify(response_object), 500
