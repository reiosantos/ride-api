"""Define custom class/method decorators to add more functionality"""

from functools import wraps

from flask import request

from api.errors.return_errors import ReturnErrors


class Decorate:
    """Define decorators to perform custom actions"""

    @staticmethod
    def receive_json(fun):
        """decorator that makes any view respond to non JSON requests"""

        @wraps(fun)
        def decorated(*args, **kwargs):
            """
            decorator implementation
            :param args:
            :param kwargs:
            :return:
            """

            if not request or not request.json:
                return ReturnErrors.not_json_request()

            return fun(*args, **kwargs)

        return decorated
