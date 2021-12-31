# encoding: utf-8
'''View that contains all of api_service's endpoints'''
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
    return clean_data

def _format_stock_data(stock_data):
    formated = {
        'name': stock_data[constants.NAME],
        'symbol': stock_data[constants.SYMBOL],
        'open': _to_int_or_float(stock_data[constants.OPEN]),
        'high': _to_int_or_float(stock_data[constants.HIGH]),
        'low': _to_int_or_float(stock_data[constants.LOW]),
        'close': _to_int_or_float(stock_data[constants.CLOSE])
    }
    return formated

def _to_int_or_float(number):
    try:
        number = int(number)
    except ValueError:
        number = float(number)
    return number

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
        UserRequestHistory.insert_stock_data(request.user, *stock_data).save()
        return Response(_format_stock_data(stock_data))


class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''Filter the queryset so that we get the records for the user making the request.'''
        # queryset = UserRequestHistory.objects.filter(user=request.user)
        # serializer_class = UserRequestHistorySerializer
        return Response()


class StatsView(APIView):
    """
    Allows super users to see which are the top-5 queried stocks.
    """
    permission_classes = (IsAdminUser,)

    def get(self, request):
        '''Implement the query needed to get the top-5 stocks as described in the README, and return
        the results to the user.'''
        return Response()
