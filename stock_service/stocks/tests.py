'''
Test for stock_service
'''
from django.test import Client, TestCase

class TestStock(TestCase):
    '''Tests for external calls'''

    def setUp(self):
        self.code = 'aapl.us'
        self.client = Client()

    def test_stock_endpoint(self):
        '''Test /stock endpoint throws'''
        response = self.client.get(f'/stock?stock_code={self.code}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, self.code in response.content.decode().lower())
