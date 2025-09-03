from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from django.contrib.auth import get_user_model

User = get_user_model()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            logout(request)
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
