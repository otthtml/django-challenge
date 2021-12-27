# encoding: utf-8
'''View that contains all of stock_service's endpoints'''
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class StockView(APIView):
    '''
    View that contains all of stock_service's endpoints
    '''
    def get(self, request):
        '''Takes a stock code, builds a request, sends it to external
        and returns result to requester'''
        stock_code = request.query_params.get('stock_code')
        query = f'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcvn&h&e=csv​'
        response = requests.request("GET", query)
        return Response(response.text)
