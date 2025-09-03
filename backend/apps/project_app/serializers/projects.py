from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.project_app.models import Project, ProjectMembership
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "description", "start_date", "end_date", "assignees", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProjectMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMembership
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class CreateProjectMembershipSerializer(serializers.Serializer):
    email = serializers.EmailField()
    project = serializers.IntegerField()

    def create(self, validated_data, invited_by) -> ProjectMembership:
        user, _ = User.objects.get_or_create(
            email=validated_data["email"],
            defaults={
                "password": "Q123123.",
            }
        )
        project = get_object_or_404(Project, id=validated_data["project"])

        project_membership, _ = ProjectMembership.objects.get_or_create(
            user=user,
            project=project,
            invited_by=invited_by,
        )

        invite_link = f"{settings.BACKEND_URL}/api/v1/projects/invite/?project_id={project.id}&project_membership_id={project_membership.id}"

        send_mail(
            subject=f"You invited to Project {project.title}",
            message=f"Click the link to accept invite: {invite_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return project_membership
