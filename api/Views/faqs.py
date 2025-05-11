from ..serializers import FAQSerializer
from ..models import FAQ
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError


class FAQView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        try:
            faq = FAQ.objects.get(id=id)
            serializer = FAQSerializer(faq, many=False)
            return Response(serializer.data)
        except FAQ.DoesNotExist:
            return Response(
                {"message":"FAQ Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, id):
        try:
            FAQ.objects.get(id=id).delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )
        except FAQ.DoesNotExist:
            return Response(
                {"message": "FAQ Not Found"}, status=status.HTTP_404_NOT_FOUND
            )





    def put(self, request, id):
        try:
            instance = FAQ.objects.get(id=id)
            serializer = FAQSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except IntegrityError:
                    return Response(
                        {"message": "A FAQ with this question already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except FAQ.DoesNotExist:
            return Response({"message": "FAQ Not Found"}, status=status.HTTP_404_NOT_FOUND)


class FAQsView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):

        faqs = FAQ.objects.all()
        paginator = PageNumberPagination()
        paginated_faqs = paginator.paginate_queryset(faqs, request)
        serializer = FAQSerializer(paginated_faqs, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
