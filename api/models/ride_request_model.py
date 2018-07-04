from api.config.database import DatabaseConnection
from api.models.rides_model import Rides
from api.utils.utils import JSONSerializable, Utils


class RideRequests:
    __table = "requests"
    __database = DatabaseConnection.connect()

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

    @classmethod
    def add_request_for_ride(cls, ride_id, passenger_id) -> bool:
        """
        create new ride request
        :param ride_id:
        :param passenger_id:
        :return:
        """

        if not ride_id:
            return False

        request_object = cls.RequestModal(ride_id=ride_id, passenger_id=passenger_id)
        data = {
            "request_id": request_object.request_id,
            "request_date": request_object.request_date,
            "ride_id_fk": request_object.ride_id,
            "passenger_id": request_object.passenger_id,
            "taken": request_object.taken,
            "status": request_object.status,
        }
        ret = cls.__database.insert(cls.__table, data)
        if not ret:
            return False
        return True

    @classmethod
    def find_one_brief_request(cls, request_id):

        criteria = {
            "request_id": request_id
        }
        response = cls.__database.find(cls.__table, criteria)
        if response and isinstance(response, dict):
            ride = cls.RequestModal(response['passenger_id'], response['ride_id_fk'])
            ride.request_id = response['request_id']
            ride.status = response['status']
            ride.taken = response['taken']
            ride.request_date = response['request_date']
            return ride
        return None

    @classmethod
    def find_all_detailed_requests(cls, driver_id, ride_id=None) -> dict or None:
        """
        fetch a detailed request including driver and passenger details
        :param ride_id:
        :param driver_id:
        :return:
        """
        if not driver_id:
            return None

        all_requests = {}

        criteria = {
            "driver_id": driver_id,
            "ride_id": ride_id
        }
        response = cls.__database.find_detailed_requests(cls.__table, criteria)
        if response and isinstance(response, list):
            for request in response:
                if request['ride_id'] not in all_requests:
                    all_requests[request['ride_id']] = []
                all_requests[request['ride_id']].append(request)

        elif ride_id and isinstance(response, dict):
            return {ride_id: response}

        return all_requests

    @classmethod
    def find_one_detailed_request(cls, req_id) -> dict or None:
        """
        fetch a single detailed ride
        :param req_id:
        :return:
        """

        criteria = {
            "request_id": req_id
        }
        response = cls.__database.find_detailed_requests(cls.__table, criteria)
        if response and isinstance(response, dict):
            return response
        return None

    @classmethod
    def approve_request_for_ride(cls, request_id) -> bool:
        """
        approve a ride offer
        :param request_id:
        :return:
        """

        return cls.update_request_status(status=cls.RequestStatus.accepted,
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
        return cls.update_request_status(status=cls.RequestStatus.rejected,
                                         request_id=request_id)

    @classmethod
    def update_request_status(cls, status, request_id, driver_id=None) -> bool:
        """
        Delegate to update ride status
        :param driver_id:
        :param status:
        :param request_id:
        :return:
        """

        if not request_id or not status:
            return False

        request = cls.find_one_brief_request(request_id)
        if not request:
            return False

        selection = {
            "request_id": request_id,
            "ride_id_fk": request.ride_id,
        }
        data = {
            "status": status or request.status
        }

        if status == cls.RequestStatus.accepted:
            ride = Rides.find_one_ride(ride_id=request.ride_id, driver_id=driver_id)
            if not ride:
                return False

            if not Rides.update_ride(ride_id=ride.ride_id,
                                     status=Rides.RideStatus.taken, driver_id=driver_id):
                return False

        return cls.__database.update(cls.__table, selection, data)

    @classmethod
    def delete_request_for_ride(cls, request_id) -> bool:
        """
        delete a request fir a ride
        :param request_id:
        :return:
        """
        if not request_id:
            return False

        selection = {
            "request_id": request_id,
        }
        return cls.__database.delete(cls.__table, selection)
