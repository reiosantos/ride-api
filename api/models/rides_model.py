"""Rides Module . Handles all rides and their possible actions"""
from typing import List

from api.config.config import DatabaseConfig
from api.config.database import DatabaseConnection
from api.utils.utils import JSONSerializable, Utils


class Rides:
    """Ride class contains ride modal and ride methods"""

    __table = "rides"
    __database = DatabaseConnection.connect(DatabaseConfig.SCHEMA_PRODUCTION)

    class RideStatus:
        """RideStatus class"""

        available = "available"
        taken = "taken"

    class RideModel(JSONSerializable):
        """Ride Modal class. It holds ride data"""

        def __init__(self, driver_id=None, destination=None, cost=0, ride_from=None, departure_time=None):
            """
            Initialize your ride
            :param driver_id:
            :param destination:
            :param cost:
            :param ride_from:
            :param departure_time:
            """
            self.ride_id = Utils.generate_ride_id()
            self.post_date = Utils.make_date_time()

            self.driver_id = driver_id
            self.destination = destination
            self.departure_time = departure_time
            self.trip_from = ride_from
            self.cost = cost
            self.status = Rides.RideStatus.available

    @classmethod
    def create_ride(cls, driver_id, destination, cost, trip_from, depart_time) -> RideModel or None:
        """
        create a new ride
        :param trip_from:
        :param destination:
        :param driver_id:
        :param cost:
        :param depart_time:
        :return RideModal:
        """
        ride = Rides.RideModel(driver_id, destination, cost, trip_from, depart_time)
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
        ret = cls.__database.insert(cls.__table, data)
        if not ret:
            return None

        return ride

    @classmethod
    def find_all_rides(cls, driver_id=None) -> List[RideModel]:
        """
        fetch all rides created" by a driver
        :param driver_id:
        :return:
        """
        if not driver_id:
            return cls.handle_query(criterion=None) or []

        criteria = {
            "driver_id": driver_id
        }
        return cls.handle_query(criteria) or []

    @classmethod
    def find_one_ride(cls, ride_id, driver_id=None) -> RideModel or None:
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
            return cls.handle_query(criteria)
        else:
            criteria = {
                "driver_id": driver_id,
                "ride_id": ride_id
            }
            return cls.handle_query(criteria)

    @classmethod
    def handle_query(cls, criterion):
        response = cls.__database.find(cls.__table, criterion)
        if response:
            if isinstance(response, list) and len(response) > 1:
                data: List[cls.RideModel] = []
                for res in response:
                    ride = cls.RideModel(res['driver_id'], res['destination'], res['trip_cost'],
                                         res['trip_from'], res['departure_time'])
                    ride.status = res['status']
                    ride.ride_id = res['ride_id']
                    ride.post_date = res['post_date']
                    data.append(ride)
                return data
            elif isinstance(response, dict) or (isinstance(response, list) and len(response) == 1):
                if isinstance(response, list):
                    response = response[0]
                ride = cls.RideModel(response['driver_id'], response['destination'], response['trip_cost'],
                                     response['trip_from'], response['departure_time'])
                ride.status = response['status']
                ride.ride_id = response['ride_id']
                ride.post_date = response['post_date']
                return ride
        return None

    @classmethod
    def update_ride(cls, ride_id, driver_id, cost=None, ride_from=None, destination=None,
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

        ride = cls.find_one_ride(ride_id, driver_id)
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
        return cls.__database.update(cls.__table, selection, data)

    @classmethod
    def delete_ride(cls, ride_id) -> bool:
        """
        delete ride
        :param ride_id:
        :return:
        """
        ride = cls.find_one_ride(ride_id)
        if not ride:
            return False
        selection = {
            "ride_id": ride_id,
        }
        return cls.__database.delete(cls.__table, selection)
