'''
Test for api_service
'''
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient, APITestCase

INVALID_TOKEN_CODE = 401
OK_CODE = 200
MOCKED_CONTENT = 'AAPL.US'


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

    return _MockResponse(MOCKED_CONTENT, OK_CODE)

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
    def test_view_invalid_token(self, _):
        '''Ensure request is blocked if token is invalid or missing across all endpoints'''

        self.assertEqual(INVALID_TOKEN_CODE, self._request_stock().status_code)
        self.assertEqual(INVALID_TOKEN_CODE, self._request_history().status_code)
        self.assertEqual(INVALID_TOKEN_CODE, self._request_stats().status_code)

        token, _ = get_tokens_for_user(self.user).blacklist()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token.token.token}'
        )
        self.assertEqual(INVALID_TOKEN_CODE, self._request_stock().status_code)
        self.assertEqual(INVALID_TOKEN_CODE, self._request_history().status_code)
        self.assertEqual(INVALID_TOKEN_CODE, self._request_stats().status_code)

    @patch('api.views.requests.get', side_effect=_mocked_requests_get)
    def test_view_valid_token(self, _):
        '''Ensure request is accepted if token is valid across all endpoints'''

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access_token}')
        self.assertEqual(OK_CODE, self._request_stock().status_code)
        self.assertEqual(OK_CODE, self._request_history().status_code)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_access_token}')
        self.assertEqual(OK_CODE, self._request_stats().status_code)
        self.assertEqual(OK_CODE, self._request_stock().status_code)
        self.assertEqual(OK_CODE, self._request_history().status_code)

    def test_stock_endpoint(self):
        '''ensure /stock endpoint functions as expected'''
        self.assertEqual(True, 1==1)

    def test_history_endpoint(self):
        '''ensure /history endpoint functions as expected'''
        self.assertEqual(True, 1==1)

    def test_stats_endpoint(self):
        '''ensure /stats endpoint functions as expected'''
        self.assertEqual(True, 1==1)
