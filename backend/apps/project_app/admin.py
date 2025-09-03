from django.contrib import admin
from apps.project_app.models import Project, Task, ProjectMembership


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "start_date", "end_date", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("start_date", "end_date", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("title", "description", "assignees", "start_date", "end_date")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "project", "status", "due_date", "version", "created_at", "updated_at")
    search_fields = ("title", "description", "project__title", "assignees__username")
    list_filter = ("status", "due_date", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("project", "title", "description", "due_date", "status", "assignees")}),
        ("Versioning", {"fields": ("version",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("version", "created_at", "updated_at")


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "project", "invited_by", "status", "joined_at", "created_at", "updated_at")

