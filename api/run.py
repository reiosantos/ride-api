# -*- coding: utf-8 -*-
"""
Main app root of the api endpoints
"""

import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT

from api.config.database import DatabaseConnection

sys.path.append(os.path.curdir)
sys.path.append(os.path.pardir)

from api.errors.request_errors import RequestError
from api.auth.user_authentication import Authenticate
from api.config.config import HostConfig, EnvironmentConfig, ServerConfig
from api.routes import Urls


class Server:
    """ Creates flask object to start the server"""

    @staticmethod
    def create_app(config=None, env=None):
        app = Flask(__name__)
        app.config.update(config.__dict__ or {})
        app.config.update(env.__dict__ or {})
        app.errorhandler(404)(RequestError.not_found)
        app.errorhandler(400)(RequestError.bad_request)
        app.errorhandler(405)(RequestError.method_not_allowed)
        app.errorhandler(500)(RequestError.internal_server_error)
        Urls.generate(app)
        CORS(app)
        with app.app_context():
            DatabaseConnection.init_db(app)
        return app


APP = Server().create_app(config=ServerConfig, env=EnvironmentConfig)

APP_JWT = JWT(APP, Authenticate.authenticate_handler, Authenticate.identity_handler)
APP_JWT.jwt_decode_callback = Authenticate.decode_auth_token
APP_JWT.jwt_encode_callback = Authenticate.encode_auth_token
APP_JWT.jwt_error_handler = RequestError.invalid_authentication_token

if __name__ == '__main__':
    APP.run(host=HostConfig.HOST, port=HostConfig.PORT)
