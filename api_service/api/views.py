# encoding: utf-8

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer


class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """
    def get(self, request, *args, **kwargs):
        '''Call the stock service, save the response, and return the response to the user'''
        stock_code = request.query_params.get('q')
        return Response()


class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    queryset = UserRequestHistory.objects.all()
    serializer_class = UserRequestHistorySerializer
    # TODO: Filter the queryset so that we get the records for the user making the request.
    def get(self, request, *args, **kwargs):
        return Response()

class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    # TODO: Implement the query needed to get the top-5 stocks as described in the README, and return
    # the results to the user.
    def get(self, request, *args, **kwargs):
        return Response()
