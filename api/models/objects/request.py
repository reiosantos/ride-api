"""
request object
"""
from api.models.objects.request_status import RequestStatus
from api.utils.utils import JSONSerializable, Utils


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
        self.status = RequestStatus.pending