"""
ride object
"""
from api.models.objects.ride_status import RideStatus
from api.utils.utils import JSONSerializable, Utils


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
        self.status = RideStatus.available
