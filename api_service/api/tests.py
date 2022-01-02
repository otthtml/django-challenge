'''
Test for api_service
'''
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient, APITestCase

from api.models import UserRequestHistory
MOCKED_CONTENT = 'Symbol,Date,Time,Open,High,Low,Close,Volume,Name\\r\\n' + \
'NVR.US,2021-12-31,22:00:37,5884.1,5917.7,5850.5,5908.87,6346,NVR\\r\\n'


def get_tokens_for_user(user):
    '''create jwt tokens for user'''
    return RefreshToken.for_user(user)

def create_user(name='octavio', email='octavio@myproject.com', password='password'):
    '''create and return an user'''
    return User.objects.create_user(name, email, password)

def create_superuser(name='admin', email='admin@myproject.com', password='password'):
    '''create and return a super user'''
    return User.objects.create_superuser(name, email, password)

def setup_user_for_tests():
    '''simple user setup for tests in all services'''
    user = create_user()
    access_token = get_tokens_for_user(user).access_token
    return user, access_token

def setup_superuser_for_tests():
    '''simple superuser setup for tests in all services'''
    superuser = create_superuser()
    access_token = get_tokens_for_user(superuser).access_token
    return superuser, access_token

def _mocked_requests_get(*_, **__):
    class _MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

    return _MockResponse(MOCKED_CONTENT, status.HTTP_200_OK)

class TestStockView(APITestCase):
    '''Tests for StockView (which make a mocked request to stock_service)'''
    def setUp(self):
        self.user, self.user_access_token = setup_user_for_tests()
        self.superuser, self.superuser_access_token = setup_superuser_for_tests()
        self.client = APIClient()

    def _request_stock(self):
        return self.client.get('/stock', {'stock_code': 'aapl.us'})

    def _request_history(self):
        return self.client.get('/history')

    def _request_stats(self):
        return self.client.get('/stats')

    @patch('api.views.requests.get', side_effect=_mocked_requests_get)
    def test_invalid_token(self, _):
        '''Ensure request is blocked if token is invalid or missing across all endpoints'''
        # ensure missing tokens are blocked
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, self._request_stock().status_code)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, self._request_history().status_code)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, self._request_stats().status_code)

        # ensure blacklisted (expired) tokens are blocked
        token, _ = get_tokens_for_user(self.user).blacklist()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.token.token}')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, self._request_stock().status_code)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, self._request_history().status_code)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, self._request_stats().status_code)

        # ensure unauthorized (regular) users are blocked
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access_token}')
        self.assertEqual(status.HTTP_403_FORBIDDEN, self._request_stats().status_code)


    @patch('api.views.requests.get', side_effect=_mocked_requests_get)
    def test_valid_token(self, _):
        '''Ensure request is accepted if token is valid across all endpoints'''

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access_token}')
        self.assertEqual(status.HTTP_200_OK, self._request_stock().status_code)
        self.assertEqual(status.HTTP_200_OK, self._request_history().status_code)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_access_token}')
        self.assertEqual(status.HTTP_200_OK, self._request_stock().status_code)
        self.assertEqual(status.HTTP_200_OK, self._request_history().status_code)
        self.assertEqual(status.HTTP_200_OK, self._request_stats().status_code)

    @patch('api.views.requests.get', side_effect=_mocked_requests_get)
    def test_stock_endpoint(self, _):
        '''ensure /stock endpoint functions as expected (cleaning, formatting and saving)'''
        initial_size = len(UserRequestHistory.objects.all())
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access_token}')
        response = self._request_stock()
        final_size = len(UserRequestHistory.objects.all())

        # ensure response is 200 and it's json
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('application/json', response.__getitem__('content-type'))

        # ensure unwanted characters were properly cleaned
        content = response.content.decode()
        self.assertEqual(-1, content.find('\\'))
        self.assertEqual(-1, content.find('\''))

        # ensure a record was inserted in the DB
        self.assertEqual(final_size, initial_size + 1)

    @patch('api.views.requests.get', side_effect=_mocked_requests_get)
    def test_history_endpoint(self, _):
        '''ensure /history endpoint functions as expected'''
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access_token}')
        response = self._request_history()

        # ensure response is 200 and it's json
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('application/json', response.__getitem__('content-type'))

    @patch('api.views.requests.get', side_effect=_mocked_requests_get)
    def test_stats_endpoint(self, _):
        '''ensure /stats endpoint functions as expected'''
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_access_token}')
        response = self._request_stats()

        # ensure response is 200 and it's json
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('application/json', response.__getitem__('content-type'))
