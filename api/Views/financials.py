from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..utils import getFinancials

class FinancialStatisticsView(APIView):

    def get(self, request, year, month, week):
        try:

            revenue_per_day = getFinancials(year, month, week, request)
            return Response(revenue_per_day)
        except ValueError as e:
            # If input parameters are invalid, return a bad request response with the error message
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)
