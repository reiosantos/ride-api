"""
Module to Handle user logout
"""
from flask import request, jsonify
from flask.views import MethodView

from api.auth.user_authentication import Authenticate


class LogoutController(MethodView):
    """
    Logout Resource
    """

    @classmethod
    def post(cls):
        """
        handle logout requests
        :return:
        """
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Authenticate.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                try:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return jsonify(response_object), 200
                except Exception as ex:
                    response_object = {
                        'status': 'fail',
                        'message': ex
                    }
                    return jsonify(response_object), 401
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return jsonify(response_object), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return jsonify(response_object), 403
