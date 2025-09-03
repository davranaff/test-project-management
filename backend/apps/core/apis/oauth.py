from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings

class OAuthView(APIView):

    def get(self, request):
        ouath_type = request.query_params.get("ouath_type", "google")

        if ouath_type == "google":
            params = f"?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri=http://localhost:8000/api/v1/login/&response_type=code&scope=email profile"
            url = "https://accounts.google.com/o/oauth2/v2/auth" + params
            return Response({"detail": url}, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid :ouath_type params"}, status=status.HTTP_400_BAD_REQUEST)