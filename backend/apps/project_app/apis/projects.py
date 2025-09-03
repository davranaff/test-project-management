from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from apps.core.permissions import admin_permission
from apps.project_app.serializers import ProjectSerializer, CreateProjectMembershipSerializer
from apps.project_app.models import Project, ProjectMembership
from apps.project_app.choices import InviteStatusChoices


User = get_user_model()


class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.get_user_projects(request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(admin_permission)
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(admin_permission)
    def put(self, request, project_id):
        with transaction.atomic():
            project = get_object_or_404(Project.objects.select_for_update(), id=project_id)
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(admin_permission)
    def delete(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectMembershiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        project_id = request.query_params.get("project_id")
        project_membership_id = request.query_params.get("project_membership_id")

        if not project_id and not project_membership_id:
            return Response({"detail": ":project_membership_id and :project_id params are required"}, status=status.HTTP_400_BAD_REQUEST)

        project_membership = get_object_or_404(ProjectMembership, id=project_membership_id)
        project = get_object_or_404(Project, id=project_id)

        with transaction.atomic():
            project.assignees.add(request.user)

            project_membership.status = InviteStatusChoices.ACCEPTED
            project_membership.joined_at = timezone.now()
            project_membership.save()

        return Response({"detail": "Invite was Accepted"}, status=status.HTTP_200_OK)

    @method_decorator(admin_permission)
    def post(self, request):
        serializer = CreateProjectMembershipSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.create(serializer.validated_data, request.user)
            return Response({"detail": "Invited"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
