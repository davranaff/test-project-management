from apps.core.apis import LoginView, RegisterView, LogoutView, VerifyEmailView, OAuthView
from apps.core.views import login_view, register_view
from django.urls import path

urlpatterns = [
    # pages
    path("login_page/", login_view, name="login_page"),
    path("register_page/", register_view, name="register_page"),

    # apis
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("oauth/", OAuthView.as_view(), name="oauth")
]
