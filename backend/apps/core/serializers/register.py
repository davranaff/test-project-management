from rest_framework.serializers import Serializer, CharField, EmailField, ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from apps.core.models import EmailVerificationToken


User = get_user_model()


class RegisterSerializer(Serializer):
    email = EmailField(required=False, allow_blank=True)
    password = CharField(write_only=True)
    confirm_password = CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

        if not email:
            raise ValidationError("You must provide either a username or an email.")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        if settings.ACCOUNT_EMAIL_VERIFICATION:
            user.is_verified = False
            user.save()
        else:
            user.is_verified = True
            user.save()

        if settings.ACCOUNT_EMAIL_VERIFICATION and user.email:
            token = EmailVerificationToken.create_token(user)
            verification_link = f"{settings.BACKEND_URL}/api/v1/verify-email/?token={token.token}"

            send_mail(
                "Verify your email",
                f"Click the link to verify your email: {verification_link}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )

        return user
