from flask import jsonify, request

from api.errors.request_errors import RequestErrors


class ReturnErrors:

    @staticmethod
    def invalid_contact():
        return jsonify({"error_message": "driver contact {0} is wrong. should be in"
                                         " the form, (0789******) and between 10 and 13 "
                                         "digits".format(request.json['contact']),
                        "data": request.json}), 400

    @staticmethod
    def invalid_password():
        return jsonify({"error_message": "Password is wrong. It should be at-least 6 characters "
                                         "long, and alphanumeric.",
                        "data": request.json}), 400

    @staticmethod
    def invalid_amount(token):
        return jsonify({"error_message": "Supplied amount {0} is wrong."
                                         " should be a number and greater than 0"
                       .format(request.json['cost']),
                        'access_token': token,
                        "data": request.json}), 400

    @staticmethod
    def missing_fields(keys, token=None):
        return jsonify({"error_message": "some of these fields are missing",
                        'access_token': token,
                        "data": keys}), 400

    @staticmethod
    def this_value_is_not_allowed(field, keys, token):
        return jsonify({"error_message": "The value provided for `{0}` is not valid."
                                         " The valid values are provided in "
                                         "data attribute:-".format(field),
                        'access_token': token,
                        "data": keys}), 400

    @staticmethod
    def empty_fields(token=None):
        return jsonify({"error_message": "some of these fields have empty/no values",
                        'access_token': token,
                        "data": request.json}), 400

    @staticmethod
    def ride_not_found(key, token):
        return jsonify({"error_message": "The requested ride {0} is not found".format(key),
                        'access_token': token,
                        "data": False}), 404

    @staticmethod
    def request_not_found(key, token):
        return jsonify({"error_message": "The requested resource {0} is not "
                                         "found".format(key),
                        'access_token': token,
                        "data": False}), 404

    @staticmethod
    def ride_already_requested(token):
        return jsonify({"error_message": "Ride {0} has been requested by another person"
                                         "".format(request.json['ride_id']),
                        'access_token': token,
                        "data": request.json}), 409

    @staticmethod
    def not_json_request():
        return RequestErrors.bad_request("Not a json request")

    @staticmethod
    def could_not_process_request(token):
        return jsonify({"error_message": "Request could not be processed.",
                        'access_token': token,
                        "data": False}), 204

    @staticmethod
    def user_not_found(token=None):
        response_object = {
            'data': False,
            'access_token': token,
            'error_message': 'User does not exist. Provide a valid phone number',
        }
        return jsonify(response_object), 404

    @staticmethod
    def not_allowed_to_perform_this_action(token):
        response_object = {
            'data': False,
            'access_token': token,
            'error_message': 'Not allowed to perform this action',
        }
        return jsonify(response_object), 401

    @staticmethod
    def user_already_exists():
        response_object = {
            'data': False,
            'error_message': 'User already exists. Please Log in.',
        }
        return jsonify(response_object), 202

    @staticmethod
    def invalid_credentials():
        response_object = {
            'data': False,
            'error_message': 'Wrong username or password.',
        }
        return jsonify(response_object), 401

    @staticmethod
    def error_occurred(token=None):
        response_object = {
            'data': False,
            'access_token': token,
            'error_message': 'Some error occurred. Please try again.'
        }
        return jsonify(response_object), 401
