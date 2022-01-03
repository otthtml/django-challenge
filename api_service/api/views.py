# encoding: utf-8
'''View that contains all of api_service's endpoints'''
from django.db.models import Count
import requests

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer
from api import constants

def _clean_stock_data(stock_data: str):
    clean_data = stock_data.split(',')
    clean_data[constants.SYMBOL] = clean_data[constants.SYMBOL].split('\\n')[1]
    clean_data[constants.NAME] = clean_data[constants.NAME].split('\\')[0]
    clean_data[constants.OPEN] = _to_int_or_float(clean_data[constants.OPEN])
    clean_data[constants.HIGH] = _to_int_or_float(clean_data[constants.HIGH])
    clean_data[constants.LOW] = _to_int_or_float(clean_data[constants.LOW])
    clean_data[constants.CLOSE] = _to_int_or_float(clean_data[constants.CLOSE])
    return clean_data

def _format_stock_data(stock_data):
    formated = {
        'name': stock_data[constants.NAME],
        'symbol': stock_data[constants.SYMBOL],
        'open': stock_data[constants.OPEN],
        'high': stock_data[constants.HIGH],
        'low': stock_data[constants.LOW],
        'close': stock_data[constants.CLOSE]
    }
    return formated

def _to_int_or_float(number):
    try:
        number = int(number)
    except ValueError:
        number = float(number)
    return round(number, 2)

def _insert_stock_data(user, *stock_data):
    UserRequestHistory.objects.create(
        user=user,
        name=stock_data[constants.NAME],
        symbol=stock_data[constants.SYMBOL],
        open=stock_data[constants.OPEN],
        high=stock_data[constants.HIGH],
        low=stock_data[constants.LOW],
        close=stock_data[constants.CLOSE],
    )  

class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''Call the stock service, clean the response, save it and return it to the user'''
        stock_code = request.query_params.get('stock_code')
        query = f'{constants.STOCK_SERVICE_URL}/stock?stock_code={stock_code}'
        stock_data = requests.get(query).text
        stock_data = _clean_stock_data(stock_data)
        _insert_stock_data(request.user, *stock_data)
        return Response(_format_stock_data(stock_data))


class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    permission_classes = (IsAuthenticated,)
    
    serializer_class = UserRequestHistorySerializer

    def get_queryset(self):
        return UserRequestHistory.objects.filter(user=self.request.user)


class StatsView(APIView):
    """
    Allows super users to see which are the top-5 queried stocks.
    """
    permission_classes = (IsAdminUser,)

    def get(self, _):
        '''Implement the query needed to get the top-5 stocks as described in the README, and return
        the results to the user.'''
        result = (UserRequestHistory.objects
            .values('symbol')
            .annotate(times_requested=Count('symbol'))
            .order_by()
        )
        return Response(result)
