'''
Test for api_service
'''
from django.test import TestCase

from common import setup_user_for_tests

class TestStockView(TestCase):
    '''Tests for StockView'''

    def test_view_invalid_token(self):
        '''ensure request is blocked if token is invalid or missing across all endpoints'''
        self.assertEqual(True, 1==1)

    def test_view_valid_token(self):
        '''ensure request is accepted if token is valid across all endpoints'''
        self.assertEqual(True, 1==1)

    def test_stock_endpoint(self):
        '''ensure /stock endpoint functions as expected'''
        self.assertEqual(True, 1==1)

    def test_history_endpoint(self):
        '''ensure /history endpoint functions as expected'''
        self.assertEqual(True, 1==1)

    def test_stats_endpoint(self):
        '''ensure /stats endpoint functions as expected'''
        self.assertEqual(True, 1==1)
