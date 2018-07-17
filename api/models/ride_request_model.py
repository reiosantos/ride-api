from api.config.database import DatabaseConnection
from api.models.objects.request import RequestModal
from api.models.objects.request_status import RequestStatus
from api.models.objects.ride_status import RideStatus
from api.models.rides_model import Rides
from api.utils.singleton import Singleton
from api.utils.utils import Utils


class RideRequests(metaclass=Singleton):
    __table = "requests"
    __database = DatabaseConnection()
    __rides = Rides()

    def add_request_for_ride(self, ride_id, passenger_id) -> bool:
        """
        create new ride request
        :param ride_id:
        :param passenger_id:
        :return:
        """

        if not ride_id:
            return False

        request_object = RequestModal(ride_id=ride_id, passenger_id=passenger_id)
        data = {
            "request_id": request_object.request_id,
            "request_date": request_object.request_date,
            "ride_id_fk": request_object.ride_id,
            "passenger_id": request_object.passenger_id,
            "taken": request_object.taken,
            "status": request_object.status,
        }
        ret = self.__database.insert(self.__table, data)
        if not ret:
            return False
        return True

    def find_one_brief_request(self, request_id):

        criteria = {
            "request_id": request_id
        }
        response = self.__database.find(self.__table, criteria)
        if response and isinstance(response, dict):
            ride = RequestModal(response['passenger_id'], response['ride_id_fk'])
            ride.request_id = response['request_id']
            ride.status = response['status']
            ride.taken = response['taken']
            ride.request_date = Utils.format_date(response['request_date'])
            return ride
        return None

    def find_all_detailed_requests(self, driver_id, ride_id=None) -> dict or None:
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
        response = self.__database.find_detailed_requests(self.__table, criteria)
        if response and isinstance(response, list):
            for request in response:
                if request['ride_id'] not in all_requests:
                    all_requests[request['ride_id']] = []
                all_requests[request['ride_id']].append(request)

        elif ride_id and isinstance(response, dict):
            return {ride_id: response}

        return all_requests

    def find_one_detailed_request(self, req_id) -> dict or None:
        """
        fetch a single detailed ride
        :param req_id:
        :return:
        """

        criteria = {
            "request_id": req_id
        }
        response = self.__database.find_detailed_requests(self.__table, criteria)
        if response and isinstance(response, dict):
            return response
        return None

    def update_request_status(self, status, request_id, driver_id=None) -> bool:
        """
        Delegate to update ride status
        :param driver_id:
        :param status:
        :param request_id:
        :return:
        """

        if not request_id or not status:
            return False

        request = self.find_one_brief_request(request_id)
        if not request:
            return False

        selection = {
            "request_id": request_id,
            "ride_id_fk": request.ride_id,
        }
        data = {
            "status": status or request.status
        }

        if status == RequestStatus.accepted:
            ride = self.__rides.find_one_ride(ride_id=request.ride_id, driver_id=driver_id)
            if not ride:
                return False

            if not self.__rides.update_ride(ride_id=ride.ride_id,
                                            status=RideStatus.taken, driver_id=driver_id):
                return False

            data['taken'] = True
        else:
            data['taken'] = False

        return self.__database.update(self.__table, selection, data)

    def delete_request_for_ride(self, request_id) -> bool:
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
        return self.__database.delete(self.__table, selection)
