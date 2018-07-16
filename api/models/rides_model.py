"""Rides Module . Handles all rides and their possible actions"""
from typing import List

from api.config.database import DatabaseConnection
from api.models.objects.ride import RideModel
from api.utils.singleton import Singleton


class Rides(metaclass=Singleton):
    """Ride class contains ride modal and ride methods"""

    __table = "rides"
    __database = DatabaseConnection()

    def create_ride(self, driver_id, destination, cost, trip_from, depart_time) -> RideModel or None:
        """
        create a new ride
        :param trip_from:
        :param destination:
        :param driver_id:
        :param cost:
        :param depart_time:
        :return RideModal:
        """
        ride = RideModel(driver_id, destination, cost, trip_from, depart_time)
        data = {
            "driver_id": ride.driver_id,
            "status": ride.status,
            "trip_cost": ride.cost,
            "trip_from": ride.trip_from,
            "departure_time": ride.departure_time,
            "destination": ride.destination,
            "post_date": ride.post_date,
            "ride_id": ride.ride_id
        }
        ret = self.__database.insert(self.__table, data)
        if not ret:
            return None

        return ride

    def find_all_rides(self, driver_id=None) -> List[RideModel]:
        """
        fetch all rides created" by a driver
        :param driver_id:
        :return:
        """
        if not driver_id:
            return self.handle_query(criterion=None) or []

        criteria = {
            "driver_id": driver_id
        }
        return self.handle_query(criteria) or []

    def find_one_ride(self, ride_id, driver_id=None) -> RideModel or None:
        """
        Fetch a single ride from a driver
        :param ride_id:
        :param driver_id:
        :return:
        """
        if not driver_id:
            criteria = {
                "ride_id": ride_id,
            }
            return self.handle_query(criteria)
        else:
            criteria = {
                "driver_id": driver_id,
                "ride_id": ride_id
            }
            return self.handle_query(criteria)

    def handle_query(self, criterion):
        response = self.__database.find(self.__table, criterion)
        if response:
            if isinstance(response, list) and len(response) > 1:
                data: List[RideModel] = []
                for res in response:
                    ride = RideModel(res['driver_id'], res['destination'], res['trip_cost'],
                                     res['trip_from'], res['departure_time'])
                    ride.status = res['status']
                    ride.ride_id = res['ride_id']
                    ride.post_date = res['post_date']
                    data.append(ride)
                return data
            elif isinstance(response, dict) or (isinstance(response, list) and len(response) == 1):
                if isinstance(response, list):
                    response = response[0]
                ride = RideModel(response['driver_id'], response['destination'], response['trip_cost'],
                                 response['trip_from'], response['departure_time'])
                ride.status = response['status']
                ride.ride_id = response['ride_id']
                ride.post_date = response['post_date']
                return ride
        return None

    def update_ride(self, ride_id, driver_id, cost=None, ride_from=None, destination=None,
                    depart_time=None, status=None) -> bool:
        """
        Update ride status and any other information
        :param ride_id:
        :param driver_id:
        :param cost:
        :param ride_from:
        :param destination:
        :param depart_time:
        :param status:
        :return:
        """

        ride = self.find_one_ride(ride_id, driver_id)
        if not ride:
            return False

        selection = {
            "ride_id": ride_id,
            "driver_id": driver_id
        }
        data = {
            "trip_cost": cost or ride.cost,
            "trip_from": ride_from or ride.trip_from,
            "destination": destination or ride.destination,
            "departure_time": depart_time or ride.departure_time,
            "status": status or ride.status
        }
        return self.__database.update(self.__table, selection, data)

    def delete_ride(self, ride_id) -> bool:
        """
        delete ride
        :param ride_id:
        :return:
        """
        ride = self.find_one_ride(ride_id)
        if not ride:
            return False
        selection = {
            "ride_id": ride_id,
        }
        return self.__database.delete(self.__table, selection)
