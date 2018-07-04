"""
    api.views
    ~~~~~~~~~~~

    This module provides class-based views inspired by the ones in flask.

    :copyright: © 2018 by reio santos.
"""
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt import jwt_required, current_identity

from api.auth.user_authentication import Authenticate
from api.errors.return_errors import ReturnErrors
from api.models.rides_model import Rides
from api.utils.decorators import Decorate
from api.utils.validators import Validators


class RidesController(MethodView):
    """A class-based view that dispatches request methods to the corresponding
       class methods. For example, if you implement a ``get`` method, it will be
       used to handle ``GET`` requests. :
    """

    @jwt_required()
    def get(self, ride_id=None):
        """
        responds to get requests
        :param ride_id:
        :return:
        """
        user = current_identity
        if hasattr(user, "password"):
            del user.password
        auth_token = Authenticate.encode_auth_token(user)

        if user:
            if ride_id:
                if user.user_type == "driver":
                    ride = Rides.find_one_ride(ride_id=ride_id, driver_id=user.user_id)
                else:
                    ride = Rides.find_one_ride(ride_id=ride_id, driver_id=None)
                if ride:
                    return jsonify({"error_message": False, "access_token": auth_token,
                                    "data": ride.__dict__})
                return ReturnErrors.ride_not_found(ride_id, auth_token)

            return jsonify({"error_message": False, "access_token": auth_token,
                            "data": [o.__dict__ for o in Rides.find_all_rides()]})

        return ReturnErrors.user_not_found(auth_token)

    @Decorate.receive_json
    @jwt_required()
    def post(self):
        """
        responds to post requests. Creating new rides
        :return:
        """
        is_driver = self.__is_driver()
        if not isinstance(is_driver, bool):
            return is_driver

        return RidesController.handel_post_new_ride()

    @staticmethod
    def handel_post_new_ride():
        """
        function break down to handle specifically requests to add new rode offers
        it breaks down from the main post function, but its still called from post
        handler
        :return:
        """
        user = current_identity
        if hasattr(user, "password"):
            del user.password
        auth_token = Authenticate.encode_auth_token(user)

        keys = ("destination", "trip_from", "cost", "depart_time")
        if not set(keys).issubset(set(request.json)):
            return ReturnErrors.missing_fields(keys, auth_token)

        if not Validators.validate_number(str(request.json['cost'])):
            return ReturnErrors.invalid_amount(auth_token)

        if not request.json["destination"] or not request.json["trip_from"]:
            return ReturnErrors.empty_fields(auth_token)

        ride = Rides.create_ride(driver_id=user.user_id,
                                 destination=request.json['destination'],
                                 trip_from=request.json['trip_from'],
                                 cost=request.json['cost'],
                                 depart_time=request.json["depart_time"])

        if ride:
            return jsonify({"success_message": "successfully added a"
                                               " new ride.",
                            "access_token": auth_token,
                            "data": True}), 201

        return ReturnErrors.error_occurred(auth_token)

    @Decorate.receive_json
    @jwt_required()
    def put(self):
        """
        responds to update requests
        It allows the driver to respond to passenger requests
        :return:
        """
        valid = self.__validate_update_request()
        if not isinstance(valid, bool):
            return valid

        user = current_identity
        if hasattr(user, "password"):
            del user.password
        auth_token = Authenticate.encode_auth_token(user)

        ride_id = request.json["ride_id"]
        ride = Rides.find_one_ride(ride_id, user.user_id)
        if not ride:
            return ReturnErrors.ride_not_found(ride_id, auth_token)

        update = Rides.update_ride(ride_id, user.user_id, request.json["cost"],
                                   request.json["trip_from"],
                                   request.json["destination"],
                                   request.json["depart_time"])
        if update:
            return jsonify({"success_message": "Update has been successful.",
                            "access_token": auth_token,
                            "data": True})

        return ReturnErrors.could_not_process_request(auth_token)

    def __validate_update_request(self):
        """
        validate request to update ride offer
        :return:
        """
        is_driver = self.__is_driver()
        if not isinstance(is_driver, bool):
            return is_driver

        user = current_identity
        if hasattr(user, "password"):
            del user.password
        auth_token = Authenticate.encode_auth_token(user)

        keys = ("ride_id", "destination", "trip_from", "cost", "depart_time")
        if not set(keys).issubset(set(request.json)):
            return ReturnErrors.missing_fields(keys, auth_token)

        if not request.json["ride_id"] or not request.json["destination"] or \
                not request.json["trip_from"] or not request.json["depart_time"]:
            return ReturnErrors.empty_fields(auth_token)

        return True

    @staticmethod
    def __is_driver():
        user = current_identity
        if not user:
            return ReturnErrors.user_not_found()

        user = current_identity
        if hasattr(user, "password"):
            del user.password
        auth_token = Authenticate.encode_auth_token(user)

        if not user.user_type == "driver":
            return ReturnErrors.not_allowed_to_perform_this_action(auth_token)

        return True

    @jwt_required()
    def delete(self, ride_id):
        """
        responds to update requests
        :return:
        """
        is_driver = self.__is_driver()
        if not isinstance(is_driver, bool):
            return is_driver

        user = current_identity
        if hasattr(user, "password"):
            del user.password
        auth_token = Authenticate.encode_auth_token(user)

        ride = Rides.find_one_ride(ride_id)
        if not ride:
            return ReturnErrors.ride_not_found(ride_id, auth_token)

        if Rides.delete_ride(ride_id):
            return jsonify({"success_message": "Ride {0} has been "
                                               "deleted.".format(ride_id),
                            "access_token": auth_token,
                            "data": True})

        return jsonify({"error_message": "Ride {0} has not been "
                                         "deleted.".format(ride_id),
                        "access_token": auth_token,
                        "data": False})
