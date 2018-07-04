import copy

from flask import request, jsonify
from flask.views import MethodView

from api.auth.user_authentication import Authenticate
from api.errors.return_errors import ReturnErrors
from api.models.users_model import Users
from api.utils.decorators import Decorate
from api.utils.validators import Validators


class RegisterController(MethodView):
    """
    User Registration Resource
    """

    @Decorate.receive_json
    def post(self):
        # get the post data
        post_data = request.get_json()

        keys = ("full_name", "contact", "username", "password", "user_type")
        if not set(keys).issubset(set(post_data)):
            return ReturnErrors.missing_fields(keys)

        contact = post_data.get('contact')
        full_name = post_data.get('full_name')
        username = post_data.get('username')
        password = post_data.get('password')
        user_type = post_data.get('user_type')

        if not Validators.validate_contact(contact):
            return ReturnErrors.invalid_contact()

        if not Validators.validate_password(password, 6):
            return ReturnErrors.invalid_password()

        # check if user already exists
        user = Users.find_user_by_contact(contact=contact)
        user_name = Users.find_user_by_username(username)
        if not user and not user_name:

            try:
                user = Users.create_user(full_name, contact, username,
                                         Authenticate.hash_password(password), user_type)

                # generate the auth token
                user = copy.deepcopy(user)
                del user.password
                auth_token = Authenticate.encode_auth_token(user)
                if isinstance(auth_token, Exception):
                    return ReturnErrors.error_occurred()

                response_object = {
                    'data': False,
                    'success_message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return jsonify(response_object), 201

            except Exception as ex:
                print(ex)
                return ReturnErrors.error_occurred()
        else:
            return ReturnErrors.user_already_exists()
