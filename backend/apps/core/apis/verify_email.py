from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from apps.core.models import EmailVerificationToken


User = get_user_model()


class VerifyEmailView(APIView):
    def get(self, request):
        token = request.query_params.get("token")

        if not token:
            return Response({"detail": ":token is required."}, status=status.HTTP_400_BAD_REQUEST)

        email = get_object_or_404(EmailVerificationToken, token=token)

        if not email.is_expired:
            return Response({"detail": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)

        email.user.verify_email()

        return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)
