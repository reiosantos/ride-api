import copy

from flask import request, jsonify
from flask.views import MethodView

from api.auth.user_authentication import Authenticate
from api.errors.return_errors import ReturnError
from api.models.users_model import Users
from api.utils.decorators import Decorate
from api.utils.validators import Validators


class RegisterController(MethodView):
    """
    User Registration Resource
    """
    __users = Users()

    @Decorate.receive_json
    def post(self):
        # get the post data
        post_data = request.get_json()

        keys = ("full_name", "contact", "username", "password", "user_type")
        if not set(keys).issubset(set(post_data)):
            return ReturnError.missing_fields(keys)

        contact = post_data.get('contact')
        full_name = post_data.get('full_name')
        username = post_data.get('username')
        password = post_data.get('password')
        user_type = post_data.get('user_type')

        if not request.json["full_name"] or not request.json["username"] \
                or not request.json["user_type"]:
            return ReturnError.empty_fields()

        if not Validators.validate_contact(contact):
            return ReturnError.invalid_contact()

        if not Validators.validate_password(password, 6):
            return ReturnError.invalid_password()

        # check if user already exists
        user = self.__users.find_user_by_contact(contact=contact)
        user_name = self.__users.find_user_by_username(username)
        if not user and not user_name:

            try:
                user = self.__users.create_user(full_name, contact, username,
                                         Authenticate.hash_password(password), user_type)

                # generate the auth token
                user = copy.deepcopy(user)
                del user.password
                auth_token = Authenticate.encode_auth_token(user)
                if isinstance(auth_token, Exception):
                    return ReturnError.error_occurred()

                response_object = {
                    'data': False,
                    'success_message': 'Successfully registered. You can now login.',
                }
                return jsonify(response_object), 201

            except Exception as ex:
                print(ex)
                return ReturnError.error_occurred()
        elif user:
            return ReturnError.contact_already_exists()
        elif user_name:
            return ReturnError.username_already_exists()
        else:
            return ReturnError.could_not_process_request()
