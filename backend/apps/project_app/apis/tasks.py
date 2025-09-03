from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db import transaction
from apps.project_app.models import Task
from apps.core.permissions import admin_permission
from apps.project_app.serializers import TaskSerializer


User = get_user_model()


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        tasks = Task.objects.get_tasks_by_project(project_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(admin_permission)
    def post(self, request, project_id):
        data = {
            **request.data,
            "project": project_id,
        }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_id, task_id):
        with transaction.atomic():
            task = get_object_or_404(Task, id=task_id)
            serializer = TaskSerializer(task, data=request.data, partial=True, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(admin_permission)
    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return Response({"detail": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
