"""
    api.views
    ~~~~~~~~~~~

    This module provides class-based views inspired by the ones in flask.

    :copyright: © 2018 by reio santos.
"""
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt import jwt_required, current_identity

from api.errors.return_errors import ReturnError
from api.models.objects.request_status import RequestStatus
from api.models.ride_request_model import RideRequests
from api.models.rides_model import Rides
from api.utils.decorators import Decorate


class RideRequestController(MethodView):
    """A class-based view that dispatches request methods to the corresponding
       class methods. For example, if you implement a ``get`` method, it will be
       used to handle ``GET`` requests. :
    """
    __rides = Rides()
    __ride_requests = RideRequests()
    __request_status = RequestStatus()

    @jwt_required()
    def get(self, ride_id=None):
        """
        responds to get requests
        :param ride_id:
        :return:
        """

        """
        is_driver = self.__is_driver()
        if not isinstance(is_driver, bool):
            return is_driver
        """

        user = current_identity
        if hasattr(user, "password"):
            del user.password

        """
        if not is_driver:
            return ReturnError.not_allowed_to_perform_this_action()
        """

        if user:
            if ride_id:
                ride = self.__rides.find_one_ride(ride_id)
                if not ride:
                    return ReturnError.ride_not_found(ride_id)

                req = self.__ride_requests.find_all_detailed_requests(user.user_id, ride_id)
                if req and (ride_id in req.keys()):
                    return jsonify({"error_message": False, "data": req[ride_id]})

                return ReturnError.request_not_found(ride_id)

            return jsonify({"error_message": False,
                            "data": [o.__dict__ for o in
                                     self.__ride_requests.find_all_detailed_requests(driver_id=user.user_id)]})

        return ReturnError.user_not_found()

    @jwt_required()
    def post(self, ride_id=None):
        """
        responds to post requests.
        :return:
        """
        return self.handle_request_ride(ride_id)

    def handle_request_ride(self, ride_id):
        """
        function break down to handle specifically requests to for response to
        ride offers from passengers offer offers
        it breaks down from the main post function, but its still called from post
        handler
        :return:
        """
        user = current_identity
        if hasattr(user, "password"):
            del user.password

        if not current_identity:
            return ReturnError.user_not_found()

        ride = self.__rides.find_one_ride(ride_id)
        if not ride:
            return ReturnError.ride_not_found(ride_id)

        req = self.__ride_requests.add_request_for_ride(ride_id, current_identity.user_id)
        if req:
            return jsonify({"success_message": "Your request has been successful. The driver"
                                               " shall be responding to you shortly",
                            "data": True}), 201

        return ReturnError.could_not_process_request()

    @Decorate.receive_json
    @jwt_required()
    def put(self, ride_id, request_id):
        """
        responds to update requests
        It allows the driver to respond to passenger requests
        :return:
        """
        valid = self.__validate_request(ride_id, request_id)
        if not isinstance(valid, bool):
            return valid
        user = current_identity
        if hasattr(user, "password"):
            del user.password

        status = request.json['status']
        keys1 = (self.__request_status.accepted, self.__request_status.rejected,
                 self.__request_status.pending)
        if status not in set(keys1):
            return ReturnError.this_value_is_not_allowed("status", keys1)

        update = self.__ride_requests.update_request_status(status, request_id,
                                                            current_identity.user_id)
        if update:
            return jsonify({"success_message": "Update has been successful.",
                            "data": True})

        return ReturnError.could_not_process_request()

    @jwt_required()
    def delete(self, ride_id, request_id):
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

        ride = self.__rides.find_one_ride(ride_id)
        if not ride:
            return ReturnError.ride_not_found(ride_id)

        req = self.__ride_requests.find_one_brief_request(request_id)
        if not req:
            return ReturnError.request_not_found(request_id)

        if self.__ride_requests.delete_request_for_ride(request_id):
            return jsonify({"success_message": "Request for Ride {0} has been "
                                               "deleted.".format(ride_id),
                            "data": True})

        return jsonify({"error_message": "Request for ride {0} has not been "
                                         "deleted.".format(ride_id),
                        "data": False})

    @staticmethod
    def __is_driver():
        user = current_identity
        if hasattr(user, "password"):
            del user.password
        if not user:
            return ReturnError.user_not_found()

        if not user.user_type == "driver":
            return ReturnError.not_allowed_to_perform_this_action()

        return True

    def __validate_request(self, ride_id, request_id):
        is_driver = self.__is_driver()
        if not isinstance(is_driver, bool):
            return is_driver

        user = current_identity
        if hasattr(user, "password"):
            del user.password

        keys = ("status",)
        if not set(keys).issubset(set(request.json)):
            return ReturnError.missing_fields(keys)

        if not request.json["status"]:
            return ReturnError.empty_fields()

        ride = self.__rides.find_one_ride(ride_id)
        if not ride:
            return ReturnError.ride_not_found(ride_id)

        req = self.__ride_requests.find_one_brief_request(request_id)
        if not req:
            return ReturnError.request_not_found(request_id)

        return True
