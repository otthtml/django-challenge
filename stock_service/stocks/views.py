# encoding: utf-8
'''View that contains all of stock_service's endpoints'''
from rest_framework.views import APIView
from rest_framework.response import Response


class StockView(APIView):
    '''
    View that contains all of stock_service's endpoints
    '''
    def get(self, request):
        '''Takes a stock code, builds a request, sends it to external
        and returns result to requester'''
        stock_code = request.query_params.get('stock_code')
        
        return Response()
