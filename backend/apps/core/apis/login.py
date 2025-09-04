import jwt
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction
from apps.core.serializers import LoginSerializer


User = get_user_model()


class LoginView(APIView):

    def get(self, request):
        code = request.query_params.get("code")

        if not code:
            return Response({"detail": ":code is required"}, status=status.HTTP_400_BAD_REQUEST)

        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URL,
            "grant_type": "authorization_code",
        }

        resp = requests.post(token_url, data=data)
        tokens = resp.json()

        if "error" in tokens:
            return Response(tokens, status=400)

        id_token = tokens.get("id_token")
        user_info = jwt.decode(id_token, options={"verify_signature": False})

        email = user_info.get("email")

        with transaction.atomic():
            user, _ = User.objects.get_or_create(
                email=email,
                defaults={"username": email},
            )
            if not user.has_usable_password():
                user.set_unusable_password()
                user.save()

            refresh = RefreshToken.for_user(user)

        redirect_params = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "name": user_info.get("name", ""),
            "picture": user_info.get("picture", ""),
        }

        redirect_url = settings.FRONTEND_REDIRECT_URL
        param_strings = [f"{key}={value}" for key, value in redirect_params.items()]
        final_url = f"{redirect_url}?{'&'.join(param_strings)}"

        return HttpResponseRedirect(redirect_to=final_url)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = None
        if username:
            user = authenticate(request, username=username, password=password)
        elif email:
            user = authenticate(request, email=email, password=password)

        if user is not None:
            if not user.is_active:
                return Response({"detail": "User account is disabled."}, status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "expires_at": refresh.access_token.payload["exp"],
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.get_full_name() or user.username,
                    "role": user.role,
                }
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
