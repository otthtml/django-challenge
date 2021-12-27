# encoding: utf-8
'''View that contains all of api_service's endpoints'''

import requests

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer

def save_stock_data(stock_data):
    '''save stock data fetched from stock_service to DB'''
    print(stock_data)


class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        '''Call the stock service, save the response, parse it and return it to the user'''
        stock_code = request.query_params.get('stock_code')
        query = f'http://localhost:8000/stock?stock_code={stock_code}'
        response = requests.request("GET", query)
        return Response('response.text')


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
