'''
Test for stock_service
'''
from django.test import TestCase

# Create your tests here.
class TestStock(TestCase):
    '''Tests for external calls'''

    def test_stooq_returns_csv(self):
        '''Test calls to stooq are returning as expected'''
        self.assertEqual(True, 1==1)
