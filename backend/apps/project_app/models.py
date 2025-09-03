from django.db import models
from apps.core.models import BaseModel, BaseOptimisticModel
from apps.project_app.choices import StatusChoices, InviteStatusChoices
from django.contrib.auth import get_user_model
from apps.project_app.querysets import ProjectQuerySet, TaskQuerySet


User = get_user_model()


class Project(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    assignees = models.ManyToManyField(
        User,
        related_name="projects",
        blank=True
    )

    objects = ProjectQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "projects"
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Task(BaseOptimisticModel):
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.TODO
    )

    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    assignees = models.ManyToManyField(
        User,
        related_name="tasks",
        null=True,
        blank=True
    )

    objects = TaskQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = "tasks"
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class ProjectMembership(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, related_name="invitations_sent", on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=InviteStatusChoices.choices, default=InviteStatusChoices.PENDING)
    joined_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"#{self.pk} - {self.user.email}, Status: {self.status}"

    class Meta:
        db_table = "project_memberships"
        unique_together = ("user", "project")
        verbose_name = "Project Membership"
        verbose_name_plural = "Project Memberships"
