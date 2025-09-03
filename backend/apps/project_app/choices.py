from django.db import models


class StatusChoices(models.TextChoices):
    TODO = "todo", "To Do"
    IN_PROGRESS = "in_progress", "In Progress"
    DONE = "done", "Done"


class InviteStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    DECLINED = "declined", "Declined"
