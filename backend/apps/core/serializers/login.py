from rest_framework.serializers import Serializer, CharField, EmailField, ValidationError


class LoginSerializer(Serializer):
    email = EmailField(required=False, allow_blank=True)
    password = CharField(write_only=True)

    def validate(self, data):
        if not data.get("email"):
            raise ValidationError("You must provide email")
        return data
