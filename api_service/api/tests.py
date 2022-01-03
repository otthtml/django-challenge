'''
Test for api_service
'''
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient, APITestCase

from api.models import UserRequestHistory

NAME = 'NVR'
SYMBOL = 'NVR.US'
OPEN = 5884.1
HIGH = 5917.7
LOW = 5850.5
CLOSE = 5908.87
MOCKED_CONTENT = 'Symbol,Date,Time,Open,High,Low,Close,Volume,Name\\r\\n' + \
f'{SYMBOL},2021-12-31,22:00:37,{OPEN},{HIGH},{LOW},{CLOSE},6346,{NAME}\\r\\n'


def _get_tokens_for_user(user):
    return RefreshToken.for_user(user)

def _create_user(name='octavio', email='octavio@myproject.com', password='password'):
    return User.objects.create_user(name, email, password)

def _create_superuser(name='admin', email='admin@myproject.com', password='password'):
    return User.objects.create_superuser(name, email, password)

def _setup_user_for_tests():
    user = _create_user()
    access_token = _get_tokens_for_user(user).access_token
    return user, access_token

def _setup_superuser_for_tests():
    superuser = _create_superuser()
    access_token = _get_tokens_for_user(superuser).access_token
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
        self.user, self.user_access_token = _setup_user_for_tests()
        self.superuser, self.superuser_access_token = _setup_superuser_for_tests()
        self.client = APIClient()

    def _request_stock(self):
        return self.client.get('/stock', {'stock_code': 'aapl.us'})

    def _request_history(self):
        return self.client.get('/history')

    def _request_stats(self):
        return self.client.get('/stats')

    def _ensure_valid_response(self, response):
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('application/json', response.__getitem__('content-type'))

    def _ensure_stock_formatted_properly(self, json_data):
        self.assertEqual(NAME, json_data['name'])
        self.assertEqual(SYMBOL, json_data['symbol'])
        self.assertEqual(OPEN, json_data['open'])
        self.assertEqual(HIGH, json_data['high'])
        self.assertEqual(LOW, json_data['low'])
        self.assertEqual(CLOSE, json_data['close'])

    @patch('api.views.requests.get', side_effect=_mocked_requests_get)
    def test_invalid_token(self, _):
        '''Ensure request is blocked if token is invalid or missing across all endpoints'''
        # ensure missing tokens are blocked
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, self._request_stock().status_code)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, self._request_history().status_code)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, self._request_stats().status_code)

        # ensure blacklisted (expired) tokens are blocked
        token, _ = _get_tokens_for_user(self.user).blacklist()
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
        stock_data = self._request_stock()
        final_size = len(UserRequestHistory.objects.all())

        # ensure unwanted characters were properly cleaned
        content = stock_data.content.decode()
        self.assertEqual(-1, content.find('\\'))
        self.assertEqual(-1, content.find('\''))

        # ensure response contains all expected fields
        json_data = stock_data.json()
        self._ensure_stock_formatted_properly(json_data)

        # ensure a record was inserted in the DB
        self.assertEqual(final_size, initial_size + 1)

        self._ensure_valid_response(stock_data)

    @patch('api.views.requests.get', side_effect=_mocked_requests_get)
    def test_history_endpoint(self, _):
        '''ensure /history endpoint functions as expected'''
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access_token}')

        # ensure history is increasing
        _ = self._request_stock()
        history_data = self._request_history()
        self.assertEqual(1, len(history_data.json()))
        _ = self._request_stock()
        history_data = self._request_history()
        self.assertEqual(2, len(history_data.json()))

        # ensure response contains all expected fields
        json_data = history_data.json()
        for i in json_data:    
            self._ensure_stock_formatted_properly(i)

        self._ensure_valid_response(history_data)

    @patch('api.views.requests.get', side_effect=_mocked_requests_get)
    def test_stats_endpoint(self, _):
        '''ensure /stats endpoint functions as expected'''
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_access_token}')

        # ensure times_requested is increasing and response contains all expected fields.
        _ = self._request_stock()
        stats_data = self._request_stats()
        stats = stats_data.json()[0]
        self.assertEqual(1, stats["times_requested"])
        self.assertEqual(SYMBOL, stats['symbol'])

        _ = self._request_stock()
        stats_data = self._request_stats()
        stats = stats_data.json()[0]
        self.assertEqual(2, stats["times_requested"])
        self.assertEqual(SYMBOL, stats['symbol'])

        self._ensure_valid_response(stats_data)
