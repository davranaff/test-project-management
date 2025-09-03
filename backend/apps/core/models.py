import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from apps.core.choices import Roles
from apps.core.querysets import BaseQuerySet, CustomUserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseQuerySet.as_manager()

    class Meta:
        abstract = True


class BaseOptimisticModel(BaseModel):
    version = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = self.__class__.objects.get(pk=self.pk)
            if original.version != self.version:
                raise ValueError("Version conflict: The record has been modified by another process.")
            self.version += 1
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.MEMBER)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def verify_email(self):
        self.is_email_verified = True
        self.save()


class EmailVerificationToken(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"#{self.pk} - {self.user.email}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def create_token(cls, user, lifetime_minutes=5):
        return cls.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=lifetime_minutes)
        )
