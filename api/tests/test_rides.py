"""
Tests module
"""
import unittest
from unittest import TestCase

from flask import json

from api.config.database import DatabaseConnection
from api.run import APP


class TestClass(TestCase):
    """
    Tests run for the api
    """

    def setUp(self):
        APP.config['TESTING'] = True
        # APP.json_encoder = CustomJSONEncoder
        self.client = APP.test_client
        self.database = DatabaseConnection()
        self.database.init_db(APP)

        res = self.client().post('/api/v1/auth/signup/', data=json.dumps(dict(
            username="flavia",
            full_name="flavia",
            contact="8976543204",
            user_type="driver",
            password="test123"
        )), content_type="application/json")
        self.assertIn(res.status_code, (201, 202))

        res = self.client().post('/api/v1/auth/login/', data=json.dumps(dict(
            username="flavia",
            password="test123",
        )), content_type="application/json")
        data = json.loads(res.data.decode("utf-8"))
        self.assertEqual(res.status_code, 200)
        self.assertIn("auth_token", data)
        self.token = data["auth_token"]

        self.headers = {
            'Authorization': "JWT {}".format(self.token)
        }

    def tearDown(self):

        self.database.drop_test_schema()

    def test_get_rides(self):
        """
        Test case for get rides endpoint, it gets all rides
        """
        res = self.client().get('/api/v1/ride/', headers=self.headers)
        self.assertEqual(res.status_code, 404)

        res = self.client().get('/api/v1/rides/', headers={
            'Authorization': "JWT {}e".format(self.token)
        })
        self.assertEqual(res.status_code, 401)

        res = self.client().get('/api/v1/rides/', headers=self.headers)

        self.assertEqual(res.status_code, 200)
        self.assertIn("error_message", res.json)
        self.assertFalse(res.json['error_message'])
        self.assertIn("data", res.json)
        self.assertIsInstance(res.json['data'], list)
        self.assertFalse(res.json["data"])

    def test_post_ride_missing(self):
        """
        Test case for get rides endpoint, it gets all rides
        """
        """missing attributes"""
        res = self.client().post('/api/v1/rides/',
                                 data=json.dumps(dict(
                                     destination="kampala",
                                     depart_time="2018-12-21",
                                     cost=3000
                                 )),
                                 headers=self.headers,
                                 content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("data", res.json)
        self.assertIn("error_message", res.json)
        self.assertIsInstance(res.json['data'], list)
        self.assertEqual(res.json['error_message'], "some of these fields are missing")

    def test_post_ride_empty(self):
        """testing empty values"""

        res = self.client().post('/api/v1/rides/',
                                 data=json.dumps(dict(
                                     destination="kampala",
                                     trip_from="",
                                     depart_time="2018-12-21",
                                     cost=3000
                                 )),
                                 headers=self.headers,
                                 content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("data", res.json)
        self.assertIn("error_message", res.json)
        self.assertIsInstance(res.json['data'], dict)
        self.assertEqual(res.json['error_message'], "some of these fields have empty/no values")

    def test_post_ride_valid(self):
        """Test successful input"""
        res = self.client().post('/api/v1/rides/',
                                 data=json.dumps(dict(
                                     destination="kampala",
                                     trip_from="Jinja",
                                     depart_time="2018-12-21",
                                     cost=3000
                                 )),
                                 headers=self.headers,
                                 content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("data", res.json)
        self.assertIn("success_message", res.json)

        res = self.client().post('/api/v1/rides/',
                                 data=json.dumps(dict(
                                     destination="kampala",
                                     trip_from="Jinja",
                                     depart_time="2018-12-21",
                                     cost=3000
                                 )),
                                 headers=self.headers,
                                 content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("data", res.json)
        self.assertIn("success_message", res.json)

        res = self.client().get('/api/v1/rides/', headers=self.headers)

        self.assertEqual(res.status_code, 200)
        self.assertIn("data", res.json)
        self.assertIsInstance(res.json['data'], list)
        self.assertTrue(len(res.json['data']) > 0)

        ride0 = res.json['data'][0]
        ride_id0 = ride0['ride_id']

        res = self.client().put(f'/api/v1/rides/',
                                data=json.dumps(dict(
                                    ride_id=ride_id0,
                                    destination="kampala",
                                    trip_from="Jinja",
                                    depart_time="2018-12-21",
                                    cost=3000
                                )),
                                headers=self.headers,
                                content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("data", res.json)
        self.assertIn("success_message", res.json)

        res = self.client().put(f'/api/v1/rides/',
                                data=json.dumps(dict(
                                    ride_id=ride_id0,
                                    trip_from="Jinja",
                                    depart_time="2018-12-21",
                                    cost=3000
                                )),
                                headers=self.headers,
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)

        res = self.client().put(f'/api/v1/rides/',
                                data=json.dumps(dict(
                                    ride_id=ride_id0,
                                    destination="",
                                    trip_from="Jinja",
                                    depart_time="2018-12-21",
                                    cost=3000
                                )),
                                headers=self.headers,
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)

        res = self.client().delete(f'/api/v1/rides/0{ride_id0}',
                                   headers=self.headers,
                                   content_type="application/json")
        self.assertEqual(res.status_code, 404)

        res = self.client().delete(f'/api/v1/rides/{ride_id0}',
                                   headers=self.headers,
                                   content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("data", res.json)
        self.assertIn("success_message", res.json)

        res = self.client().post(f'/api/v1/rides/1/requests/',
                                 headers=self.headers,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 404)
        self.assertIn("data", res.json)
        self.assertIn("error_message", res.json)
        self.assertFalse(res.json['data'])
        self.assertEqual(res.json['error_message'], 'The requested ride 1 is not found')

        res = self.client().get('/api/v1/rides/', headers=self.headers)
        self.assertEqual(res.status_code, 200)
        self.assertIn("data", res.json)
        self.assertIsInstance(res.json['data'], list)
        self.assertTrue(len(res.json['data']) > 0)

        ride = res.json['data'][0]
        ride_id = ride['ride_id']

        res = self.client().post(f'/api/v1/rides/{ride_id}/requests/',
                                 headers=self.headers,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client().post(f'/api/v1/rides/{ride_id}/requests/',
                                 headers=self.headers,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 201)

        res = self.client().get(f'/api/v1/rides/{ride_id}/requests/',
                                headers=self.headers,
                                content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn("data", res.json)
        requ = res.json['data'][0]
        requ_id = requ['request_id']

        res = self.client().put(f'/api/v1/rides/{ride_id}/requests/0{requ_id}',
                                data=json.dumps(dict(
                                    status="accept",
                                )),
                                headers=self.headers,
                                content_type='application/json')
        self.assertEqual(res.status_code, 404)

        res = self.client().put(f'/api/v1/rides/{ride_id}/requests/{requ_id}',
                                data=json.dumps(dict(
                                    status="accept",
                                )),
                                headers=self.headers,
                                content_type='application/json')
        self.assertEqual(res.status_code, 400)

        res = self.client().put(f'/api/v1/rides/{ride_id}/requests/{requ_id}',
                                data=json.dumps(dict(
                                    status="accepted",
                                )),
                                headers=self.headers,
                                content_type='application/json')
        self.assertEqual(res.status_code, 200)

        res = self.client().put(f'/api/v1/rides/{ride_id}/requests/{requ_id}',
                                data=json.dumps(dict(
                                    status="rejected",
                                )),
                                headers=self.headers,
                                content_type='application/json')
        self.assertEqual(res.status_code, 200)

        res = self.client().delete(f'/api/v1/rides/{ride_id}/requests/{requ_id}',
                                headers=self.headers,
                                content_type='application/json')
        self.assertEqual(res.status_code, 200)

        res = self.client().get(f'/api/v1/rides/0{ride_id}/requests/',
                                   headers=self.headers,
                                   content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def test_update_ride(self):
        """
        Test case for ride requests endpoint, it tests updates to a rides
        """
        res = self.client().post('/api/v1/rides/',
                                 data=json.dumps(dict(
                                     destination="kampala",
                                     trip_from="Jinja",
                                     depart_time="2018-12-21",
                                     cost=3000
                                 )),
                                 headers=self.headers,
                                 content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("data", res.json)
        self.assertIn("success_message", res.json)
        self.assertEqual(res.json['success_message'], "successfully added a new ride.")

        res = self.client().get('/api/v1/rides/', headers=self.headers)

        self.assertEqual(res.status_code, 200)
        self.assertIn("data", res.json)
        self.assertIsInstance(res.json['data'], list)
        self.assertTrue(len(res.json['data']) > 0)

        ride = res.json['data'][0]
        ride_id = ride['ride_id']

        res = self.client().post(f'/api/v1/rides/{ride_id}/requests/',
                                 headers=self.headers,
                                 content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn("data", res.json)
        self.assertNotIn("error_message", res.json)
        self.assertIn("success_message", res.json)

        res = self.client().get(f'/api/v1/rides/{ride_id}/requests/',
                                headers=self.headers,
                                content_type='application/json')
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
