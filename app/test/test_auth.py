import unittest
import json
from app.test.base import BaseTestCase
from flask_api import status


def register_user(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email='test@mail.com',
            username='test',
            password='test123'
        )),
        content_type='application/json'
    )

def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='test@mail.com',
            password='test123'
        )),
        content_type='application/json'
    )


class TestAuth(BaseTestCase):

    def test_registered_user_login(self):
        with self.client:
            user_response=register_user(self)
            response_data=json.loads(user_response.data.decode())
            self.assertTrue(response_data.get('Authorization'))
            self.assertEqual(user_response.status_code,status.HTTP_201_CREATED)

            #login user
            login_response=login_user(self)
            login_data=json.loads(login_response.data.decode())
            self.assertTrue(login_data.get('Authorization'))
            self.assertEqual(login_response.status_code,status.HTTP_200_OK)

    def test_valid_logout(self):
        with self.client:
            user_response = register_user(self)
            response_data = json.loads(user_response.data.decode())
            self.assertTrue(response_data.get('Authorization'))
            self.assertEqual(user_response.status_code, status.HTTP_201_CREATED)

            # login user
            login_response = login_user(self)
            login_data = json.loads(login_response.data.decode())
            self.assertTrue(login_data.get('Authorization'))
            self.assertEqual(login_response.status_code, status.HTTP_200_OK)

            #logout valid user
            response=self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer '+json.loads(login_response.data.decode())['Authorization']
                )
            )

            data=json.loads(response.data.decode())
            self.assertTrue(data.get('status'),'success')
            self.assertEqual(response.status_code,status.HTTP_200_OK)


if __name__ == '__main__':
    unittest.main()