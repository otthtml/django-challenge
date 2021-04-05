# encoding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response


class StockView(APIView):
    """
    Receives stock requests from the API service.
    """
    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('stock_code')
        # TODO: Make request to the stooq.com API, parse the response and send it to the API service.
        return Response()
