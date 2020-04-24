import unittest
import json
from app.test.base import BaseTestCase
from flask_api import status
from app.main.model.user import User


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

def get_books(self):
    return self.client.get(
        '/book/',
        data=json.dumps(dict(
        )),
        content_type='application/json'
    )


def save_books(self,token):
    req_data=dict()
    req_data['name']='test'
    req_data['author']='auth_test'
    req_data['description']='desc test'
    return self.client.post(
        '/book/',
        data=json.dumps(req_data),
        content_type='application/json',
        headers={'Authorization': token}
    )

class TestBookList(BaseTestCase):

    def test_booklist_getall(self):
        with self.client:
            resp=get_books(self)
            self.assertEqual(resp.status_code,status.HTTP_200_OK)



    def test_booklist_save_with_valid_autherization(self):
        with self.client:
            user_response=register_user(self)
            response_data = json.loads(user_response.data.decode())
            auth_token=response_data.get('Authorization')
            book_resp = save_books(self, auth_token)
            book_data=json.loads(book_resp.data.decode())

            self.assertEqual(book_resp.status_code,status.HTTP_201_CREATED)
            self.assertEqual(book_data.get('status'),'success')

    def test_booklist_save_without_authorizatin(self):
        with self.client:
            register_user(self)
            user = User.query.filter_by(email='test@mail.com').first()
            resp=save_books(self,'')
            self.assertEqual(resp.status_code,status.HTTP_401_UNAUTHORIZED)





if __name__ == '__main__':
    unittest.main()
