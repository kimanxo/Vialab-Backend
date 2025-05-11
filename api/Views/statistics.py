from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from api.models import Feedback, Order
from api.utils import (
    getMostOrdered,
    getTodayRevenue,
    getSexStats,
    getAgeStats,
    getFrequentExams,
    getRecentClients,
)
from django.utils import timezone


class StatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(
            {
                "orders": Order.objects.filter(
                    ordered_at__date=timezone.now().date()
                ).count(),
                "messages": Feedback.objects.filter(
                    sent_at__date=timezone.now().date()
                ).count(),
                "mostOrdered": getMostOrdered(),
                "todayRevenue": getTodayRevenue(),
                "sexStats": getSexStats(),
                "ageStats": getAgeStats(),
                "frequentExams": getFrequentExams(),
                "recentClients": getRecentClients(),
            }, status=  status.HTTP_200_OK
        )
