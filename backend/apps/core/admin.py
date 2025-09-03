from apps.core.models import EmailVerificationToken
from django.contrib.auth import get_user_model
from django.contrib import admin

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active", "is_email_verified", "is_staff", "is_superuser", "role")
    search_fields = ("username", "email")
    list_filter = ("is_active", "is_email_verified", "is_staff", "is_superuser")
    ordering = ("username",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_email_verified", "is_staff", "is_superuser", "groups", "user_permissions", "role")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("last_login", "date_joined")


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "expires_at",)
    search_fields = ("user",)
    list_filter = ("user", "token", "expires_at",)
    ordering = ("user",)
    readonly_fields = ("created_at", "updated_at",)
