from api.utils.utils import JSONSerializable, Utils


class UserModel(JSONSerializable):
    """ User modal to hold user data"""

    def __init__(self, full_name=None, contact=None, username=None,
                 password=None, user_type=None):
        """
        user modal template
        :param full_name:
        :param contact:
        :param username:
        :param password:
        :param user_type:
        """
        self.user_id = Utils.generate_user_id()
        self.registration_date = Utils.make_date_time()

        self.full_name = full_name
        self.username = username
        self.contact = contact
        self.password = password
        self.user_type = user_type

    def __str__(self):
        return "User(id='%s')" % self.user_id
