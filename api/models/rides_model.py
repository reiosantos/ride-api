"""Rides Module . Handles all rides and their possible actions"""
from typing import List

from api.utils.utils import JSONSerializable, Utils


class Rides:
    """Ride class contains ride modal and ride methods"""

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

    rides: List[RideModel] = []

    @staticmethod
    def create_ride(driver_id, destination, cost, trip_from, depart_time) -> RideModel:
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
        Rides.rides.append(ride)
        return ride

    @classmethod
    def find_all_rides(cls, driver_id=None) -> List[RideModel]:
        """
        fetch all rides created" by a driver
        :param driver_id:
        :return:
        """
        if not driver_id:
            return cls.rides

        my_rides = []
        for ride in cls.rides:
            if ride.driver_id == driver_id:
                my_rides.append(ride)
        return my_rides

    @classmethod
    def find_one_ride(cls, ride_id, driver_id=None) -> RideModel or None:
        """
        Fetch a single ride from a driver
        :param ride_id:
        :param driver_id:
        :return:
        """

        if not driver_id:
            for ride in Rides.rides:
                if ride.ride_id == ride_id:
                    return ride
        else:
            for ride in Rides.rides:
                if ride.ride_id == ride_id and ride.driver_id == driver_id:
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
        index = cls.rides.index(ride)

        cls.rides.remove(ride)

        ride.cost = cost or ride.cost
        ride.trip_from = ride_from or ride.trip_from
        ride.destination = destination or ride.destination
        ride.departure_time = depart_time or ride.departure_time
        ride.status = status or ride.status

        cls.rides.insert(index, ride)
        return True

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

        cls.rides.remove(ride)
        return True
