from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth.models import User

# an endpoint for changing the password
class ChangePasswordView(APIView):
    permission_classes = [
        permissions.IsAdminUser
    ]  # only admins can perform this operation

    def post(self, request):
        user = request.user
        if user.check_password(
            request.data["current_password"]
        ):  # verifying the old passord correctness
            user.set_password(request.data["new_password"])  # performing the operation
            user.save()

            return Response({"message":"password changed successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"wrong current password"}, status=status.HTTP_400_BAD_REQUEST)


