from ..serializers import AboutSerializer
from ..models import About
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class AboutView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        about = About.objects.first()
        if not about:
            return Response(
                {"message": "No about information found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = AboutSerializer(about)
        return Response(serializer.data)

    def put(self, request):
        about = get_object_or_404(About, id=1)
        serializer = AboutSerializer(about, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
