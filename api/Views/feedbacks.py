from ..serializers import FeedbackSerializer
from ..models import Feedback
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class FeedbacksView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):

        feedbacks = Feedback.objects.all()
        paginator = PageNumberPagination()
        paginated_feedbacks = paginator.paginate_queryset(feedbacks, request)
        serializer = FeedbackSerializer(paginated_feedbacks, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        try:
            feedback = Feedback.objects.get(id=id)
            serializer = FeedbackSerializer(feedback, many=False)
            return Response(serializer.data)
        except Feedback.DoesNotExist:
            return Response(
                {"message":"Feedback Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, id):
        try:
            Feedback.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT
            )
        except Feedback.DoesNotExist:
            return Response(
                {"message": "Feedback Not Found"}, status=status.HTTP_404_NOT_FOUND
            )


    def put(self, request, id):
        try:
            feedback = Feedback.objects.get(id=id)
            serializer = FeedbackSerializer(feedback, data=request.data, partial=True)

            if serializer.is_valid():
                # Mark feedback as read when updating
                serializer.validated_data["read"] = True
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Feedback.DoesNotExist:
            return Response(
                {"message": "Feedback Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
