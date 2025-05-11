from ..serializers import ExamSerializer
from ..models import Exam
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError

class ExamView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        try:
            exam = Exam.objects.get(id=id)
            serializer = ExamSerializer(exam, many=False)
            return Response(serializer.data)
        except Exam.DoesNotExist:
            return Response({"message":"Exam Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            exam = Exam.objects.get(id=id)
            exam.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exam.DoesNotExist:
            return Response(
                {"message": "Exam Not Found"}, status=status.HTTP_404_NOT_FOUND
            )





    def put(self, request, id):
        try:
            exam = Exam.objects.get(id=id)
            serializer = ExamSerializer(exam, data=request.data, partial=True)

            if serializer.is_valid():
                try:
                    # Ensure price is positive before saving
                    if "price" in serializer.validated_data:
                        serializer.validated_data["price"] = abs(
                            float(serializer.validated_data["price"])
                        )

                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except IntegrityError:
                    return Response(
                        {"message": "A conflict occurred while updating the exam."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exam.DoesNotExist:
            return Response({"message": "Exam Not Found"}, status=status.HTTP_404_NOT_FOUND)


class ExamsView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):

        exams = Exam.objects.all()
        paginator = PageNumberPagination()
        paginated_exams = paginator.paginate_queryset(exams, request)
        serializer = ExamSerializer(paginated_exams, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = ExamSerializer(data=data)
        if serializer.is_valid():
    
            data["abbrv"] = data.get("abbrv").upper()
            data["_type"] = data["_type"].upper()
            data["price"] = abs(float(data["price"]))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvailableExamsView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        exam = Exam.objects.filter(available=True)
        paginator = PageNumberPagination()
        paginated_exams = paginator.paginate_queryset(exam, request)
        serializer = ExamSerializer(paginated_exams, many=True)
        return paginator.get_paginated_response(serializer.data)
