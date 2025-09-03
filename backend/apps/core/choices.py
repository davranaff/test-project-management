from django.db import models


class Roles(models.TextChoices):
    ADMIN = "admin", "Admin"
    MEMBER = "member", "Member"
