'''
Common functions used across all services
'''
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    '''create jwt tokens for user'''
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def create_user(name='octavio', email='octavio@myproject.com', password='password'):
    '''create and return an user'''
    return User.objects.create_user(name, email, password)

def create_superuser(name='admin', email='admin@myproject.com', password='password'):
    '''create and return a super user'''
    return User.objects.create_superuser(name, email, password)

def setup_user_for_tests():
    '''simple user setup for tests in all services'''
    user = create_user()
    get_tokens_for_user(user)

def setup_superuser_for_tests():
    '''simple superuser setup for tests in all services'''
    superuser = create_superuser()
    get_tokens_for_user(superuser)
