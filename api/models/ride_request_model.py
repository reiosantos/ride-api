from typing import List

from api.models.rides_model import Rides
from api.models.users_model import Users
from api.utils.utils import JSONSerializable, Utils


class RideRequests:
    class RequestStatus:
        pending = "pending"
        accepted = "accepted"
        rejected = "rejected"

    class RequestModal(JSONSerializable):
        """Ride request modal."""

        def __init__(self, passenger_id=None, ride_id=None):
            """
            ride request modal
            :param passenger_id:
            :param ride_id:
            """
            self.request_id = Utils.generate_request_id()
            self.request_date = Utils.make_date_time()

            self.ride_id = ride_id
            self.passenger_id = passenger_id
            self.taken = False
            self.status = RideRequests.RequestStatus.pending

    requests: List[RequestModal] = []

    @classmethod
    def find_one_brief_request(cls, request_id):
        for req in cls.requests:
            if req.request_id == request_id:
                return req
        return None

    @classmethod
    def find_all_detailed_requests(cls, driver_id) -> dict or None:
        """
        fetch a detailed request including driver and passenger details
        :param driver_id:
        :return:
        """
        if not driver_id:
            return None
        all_requests = {}

        for request in cls.requests:
            ride = Rides.find_one_ride(request.ride_id, driver_id=driver_id)
            if ride:
                passenger = Users.find_user_by_id(request.passenger_id)
                if passenger:
                    del passenger.password
                    del passenger.user_id
                    if ride.ride_id not in all_requests:
                        all_requests[ride.ride_id] = {}
                    all_requests[ride.ride_id].update(request.__dict__)
                    all_requests[ride.ride_id].update(ride.__dict__)
                    all_requests[ride.ride_id].update(passenger.__dict__)

        return all_requests

    @classmethod
    def find_one_detailed_request(cls, req_id) -> dict or None:
        """
        fetch a single detailed ride
        :param req_id:
        :return:
        """

        for request in RideRequests.requests:
            if request.request_id == req_id:
                ride = Rides.find_one_ride(request.ride_id)
                if ride:
                    passenger = Users.find_user_by_id(request.passenger_id)
                    if passenger:
                        request_object = {}
                        request_object.update(request.__dict__)
                        request_object.update(ride.__dict__)
                        request_object.update(passenger.__dict__)
                        return request_object
        return {}

    @classmethod
    def add_request_for_ride(cls, ride_id, passenger_id) -> bool:
        """
        create new ride requesr
        :param ride_id:
        :param passenger_id:
        :return:
        """

        if not ride_id:
            return False

        request_object = cls.RequestModal(ride_id=ride_id, passenger_id=passenger_id)
        cls.requests.append(request_object)
        return True

    @classmethod
    def approve_request_for_ride(cls, request_id) -> bool:
        """
        approve a ride offer
        :param request_id:
        :return:
        """

        return cls.__update_request_status(status=cls.RequestStatus.accepted,
                                           request_id=request_id)

    @classmethod
    def reject_request_for_ride(cls, request_id) -> bool:
        """
        reject a ride request
        :param request_id:
        :return:
        """

        if not request_id:
            return False
        return cls.__update_request_status(status=cls.RequestStatus.rejected,
                                           request_id=request_id)

    @classmethod
    def update_request_status(cls, status, request_id) -> bool:
        """
        Delegate to update ride status
        :param status:
        :param request_id:
        :return:
        """

        if not request_id or not status:
            return False

        request = cls.find_one_brief_request(request_id)

        if not request:
            return False
        index = cls.requests.index(request)

        if status == cls.RequestStatus.accepted:
            ride = Rides.find_one_ride(ride_id=request.ride_id)
            if not ride:
                return False
            if not Rides.update_ride(ride_id=ride.ride_id,
                                     status=Rides.RideStatus.taken, driver_id=None):
                return False
            request.taken = True

        request.status = status

        cls.requests.remove(request)
        cls.requests.insert(index, request)
        return True

    @classmethod
    def delete_request_for_ride(cls, request_id) -> bool:
        """
        delete a request fir a ride
        :param request_id:
        :return:
        """
        if not request_id:
            return False

        req = cls.find_one_brief_request(request_id)
        if req:
            cls.requests.remove(req)
            return True
        return False
