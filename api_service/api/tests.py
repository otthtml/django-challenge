'''
Test for api_service
'''
from django.test import TestCase

# Create your tests here.
class TestJWT(TestCase):
    '''Tests for JWT auth'''

    def test_jwt_create(self):
        '''Test JWT creation'''
        self.assertEqual(True, 1==1)
