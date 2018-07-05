import unittest

from flask import json

from api.config.database import DatabaseConnection
from api.run import APP


class TestRegistration(unittest.TestCase):

    def setUp(self):
        APP.config['TESTING'] = True
        self.client = APP.test_client
        DatabaseConnection.init_db(APP)
        self.database = DatabaseConnection.connect()
        self.database.create_test_schema()
        self.token = None

    def tearDown(self):
        self.database.drop_test_schema()

    def test_missing_attributes(self):
        """
        Tests missing attributes in json request (not values)
        :return:
        """
        res = self.client().post('/api/v1/auth/signup/', data=json.dumps(dict(
            username="flavia",
            contact="345678",
            user_type="driver",
            password="password"
        )), content_type="application/json")
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(res.status_code, 400)
        self.assertIn("error_message", data)
        self.assertTrue(data['error_message'])

    def test_empty_values(self):
        """
        Testing empty or missing values
        :return:
        """
        res = self.client().post('/api/v1/auth/signup/', data=json.dumps(dict(
            username="flavia",
            full_name="",
            contact="345678",
            user_type="driver",
            password=""
        )), content_type="application/json")
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(res.status_code, 400)
        self.assertIn("error_message", data)
        self.assertTrue(data['error_message'])

    def test_invalid_contact(self):
        """
        testing invalid contact
        :return:
        """
        res = self.client().post('/api/v1/auth/signup/', data=json.dumps(dict(
            username="flavia",
            full_name="flavia",
            contact="345678",
            user_type="driver",
            password=""
        )), content_type="application/json")
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(res.status_code, 400)
        self.assertIn("error_message", data)
        self.assertTrue(data['error_message'])

    def test_minimum_length_password(self):
        """
        valid data for registration
        :return:
        """
        res = self.client().post('/api/v1/auth/signup/', data=json.dumps(dict(
            username="flavia",
            full_name="flavia",
            contact="345678",
            user_type="driver",
            password="test"
        )), content_type="application/json")
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(res.status_code, 400)
        self.assertIn("error_message", data)
        self.assertTrue(data['error_message'])

    def test_valid_registration_and_login(self):
        """ Test for user registration """

        res = self.client().post('/api/v1/auth/signup/', data=json.dumps(dict(
            username="flavia",
            full_name="flavia",
            contact="0897654324",
            user_type="driver",
            password="test123"
        )), content_type="application/json")
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(res.status_code, 201)
        self.assertNotIn("error_message", data)
        self.assertIn("success_message", data)
        self.assertEqual(data['success_message'], 'Successfully registered.')

        res = self.client().post('/api/v1/auth/login/', data=json.dumps(dict(
            username="flavi",
            password="test12",
        )), content_type="application/json")
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(res.status_code, 404)
        self.assertIn("error_message", data)
        self.assertEqual(data['error_message'], 'User does not exist. '
                                                'Provide a valid phone number')

        res = self.client().post('/api/v1/auth/login/', data=json.dumps(dict(
            username="flavia",
            password="test12",
        )), content_type="application/json")
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(res.status_code, 401)
        self.assertIn("error_message", data)
        self.assertEqual(data['error_message'], 'Wrong username or password.')

        res = self.client().post('/api/v1/auth/login/', data=json.dumps(dict(
            username="flavia",
            password="test123",
        )), content_type="application/json")
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(res.status_code, 200)
        self.assertIn("auth_token", data)
        self.assertIn("success_message", data)
        self.assertEqual(data['success_message'], 'Successfully logged in.')

        self.token = data['auth_token']

        # valid token logout
        response = self.client().post(
            'api/v1/auth/logout',
            headers=dict(
                Authorization='Bearer ' + self.token
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged out.')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
