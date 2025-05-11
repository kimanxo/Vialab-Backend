from api.serializers import OrderSerializer, OrderCleanSerializer
from api.models import Order
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from api.utils import generateCode

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class OrderCheckView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            code = request.data["code"]
            order = Order.objects.get(code=code)
            done = order.done
            email = order.email or None
            if request.data.get("email") :
                order.email = request.data["email"]
                return Response({"done": done, "email": email})
            return Response({"done": done,"email": email})

        except Order.DoesNotExist:
            return Response(
                {"message":"Order Not Found"}, status=status.HTTP_404_NOT_FOUND
            )


class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        try:
            order = Order.objects.get(id=id)
            serializer = OrderSerializer(order, many=False)
            data = serializer.data
            return Response(data)

        except Order.DoesNotExist:
            return Response(
                {"message": "Order Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, id):
        try:
            Order.objects.get(id=id).delete()
            return Response(
                 status=status.HTTP_204_NO_CONTENT
            )
        except Order.DoesNotExist:
            return Response(
                {"message": "Order Not Found"}, status=status.HTTP_404_NOT_FOUND
            )

    

    def put(self, request, id):
        try:
            instance = Order.objects.get(id=id)
            serializer = OrderSerializer(instance, data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                # Convert 'patient' field to uppercase if provided
                if "patient" in validated_data:
                    validated_data["patient"] = validated_data["patient"].upper()

                # Handle Many-to-Many relationship for 'exam' if provided
                if "exam" in request.data:
                    instance.exam.set(request.data["exam"])

                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Order.DoesNotExist:
            return Response({"message": "Order Not Found"}, status=status.HTTP_404_NOT_FOUND)

class OrdersView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):

        orders = Order.objects.prefetch_related().all()
        paginator = PageNumberPagination()
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = OrderCleanSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data
        data["code"] = generateCode()
        serializer = OrderSerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderEmailView(APIView):
    def post(self, request):
        code = request.data.get("code")
        email = request.data.get("email")

        # Validate required fields
        if not code or not email:
            return Response(
                {"message": "Both 'code' and 'email' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"message": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(code=code)
            order.email = email
            order.save()
            return Response({"message": "Email Updated"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(
                {"message": "Order Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
