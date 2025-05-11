from ..serializers import AnnounceSerializer
from ..models import Announce
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class AnnouncementsView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):

        announcements = Announce.objects.all()
        paginator = PageNumberPagination()
        paginated_announcements = paginator.paginate_queryset(announcements, request)
        serializer = AnnounceSerializer(paginated_announcements, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = AnnounceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnnouncementView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        try:
            announcement = Announce.objects.get(id=id)
            serializer = AnnounceSerializer(announcement)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Announce.DoesNotExist:
            return Response(
                {"message": "Announcement Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, id):
        try:
            announcement = Announce.objects.get(id=id)
            announcement.delete()
            return Response(
                {"message": "Announcement deleted successfully."},
                status=status.HTTP_200_OK,
            )
        except Announce.DoesNotExist:
            return Response(
                {"message": "Announcement Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, id):
        try:
            announcement = Announce.objects.get(id=id)
            serializer = AnnounceSerializer(announcement, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Announce.DoesNotExist:
            return Response(
                {"message": "Announcement Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
