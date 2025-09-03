from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.db import transaction


User = get_user_model()


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.create(serializer.validated_data)
            return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
