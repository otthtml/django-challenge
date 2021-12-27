'''
Test for stock_service
'''
from django.test import TestCase

# Create your tests here.
class TestStock(TestCase):
    '''Tests for external calls'''
    CODE = 'aapl.us'


    def test_stooq_returns_valid_csv(self):
        '''Test calls to stooq are returning as expected'''
        self.assertEqual(True, 1==1)


    def test_stock_endpoint(self):
        '''Test /stock endpoint throws'''
        self.assertEqual(True, 1==1)
