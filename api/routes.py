"""
Urls class , to handel request urls,
"""
from api.views.login_view import LoginController
from api.views.logout_view import LogoutController
from api.views.register_view import RegisterController
from api.views.requests_view import RideRequestController
from api.views.rides_view import RidesController


class Urls:
    """
    Class to generate urls via static method generate
    """

    @staticmethod
    def generate(app):
        """
        Generate urls on the app context
        It takes no argument
        :param: app: takes in the app variable
        :return: urls
        """

        """Ride offers routes"""
        app.add_url_rule('/api/v1/rides/', view_func=RidesController.as_view('get_rides'), methods=['GET'],
                         strict_slashes=False)
        app.add_url_rule('/api/v1/rides/', view_func=RidesController.as_view('post_ride'), methods=["POST"],
                         strict_slashes=False)
        app.add_url_rule('/api/v1/rides/', view_func=RidesController.as_view('update_a_ride'),
                         methods=['PUT'], strict_slashes=False)
        app.add_url_rule('/api/v1/rides/<string:ride_id>/', view_func=RidesController.as_view('get_one_ride'),
                         methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/rides/<string:ride_id>/', view_func=RidesController.as_view('delete_a_ride'),
                         methods=['DELETE'], strict_slashes=False)

        """Routes for ride requests"""
        app.add_url_rule('/api/v1/rides/<string:ride_id>/requests/', view_func=RideRequestController.
                         as_view('request_join_ride'), methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v1/rides/<string:ride_id>/requests/', view_func=RideRequestController.
                         as_view('view_ride_request'), methods=['GET'], strict_slashes=False)
        app.add_url_rule('/api/v1/rides/<string:ride_id>/requests/<string:request_id>/',
                         view_func=RideRequestController.as_view('delete_ride_request'),
                         methods=['DELETE'], strict_slashes=False)
        app.add_url_rule('/api/v1/rides/<string:ride_id>/requests/<string:request_id>/',
                         view_func=RideRequestController.as_view('update_ride_request'),
                         methods=['PUT'], strict_slashes=False)

        """authentication routes"""
        app.add_url_rule('/api/v1/auth/signup/', view_func=RegisterController.as_view('sign_up_user'),
                         methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/login/', view_func=LoginController.as_view('log_in_user'),
                         methods=['POST'], strict_slashes=False)
        app.add_url_rule('/api/v1/auth/logout/', view_func=LogoutController.as_view('log_out_user'),
                         methods=['POST'], strict_slashes=False)
