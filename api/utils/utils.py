import json
from datetime import datetime


class Utils:

    @staticmethod
    def make_date_time() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def __create_unique_number():
        return datetime.now().strftime("%Y%m%d%H%M%S%f")

    @staticmethod
    def generate_request_id():
        return "RQT" + Utils.__create_unique_number()

    @staticmethod
    def generate_ride_id():
        return "RID" + Utils.__create_unique_number()

    @staticmethod
    def generate_user_id():
        return "USR" + Utils.__create_unique_number()

    @classmethod
    def format_date(cls, param: datetime):
        return param.strftime("%Y-%m-%d %H:%M:%S")


class JSONSerializable(object):

    def to_json(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.to_json()
