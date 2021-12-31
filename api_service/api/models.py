# enconding: utf-8

from django.conf import settings
from django.db import models
from api import constants

class UserRequestHistory(models.Model):
    """
    Model to store the requests done by each user.
    """
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @classmethod
    def insert_stock_data(cls, user, *stock_data):
        return cls(
            user=user,
            name=stock_data[constants.NAME],
            symbol=stock_data[constants.SYMBOL],
            open=stock_data[constants.OPEN],
            high=stock_data[constants.HIGH],
            low=stock_data[constants.LOW],
            close=stock_data[constants.CLOSE],
        )
