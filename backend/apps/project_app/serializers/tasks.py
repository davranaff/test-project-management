from rest_framework import serializers
from apps.project_app.models import Task
from apps.core.choices import Roles



class TaskSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user and getattr(user, "role", None) == Roles.MEMBER.value:
            if set(validated_data.keys()) != {"status"}:
                raise serializers.ValidationError(
                    {"detail": "Members can only update the status field."}
                )

        return super().update(instance, validated_data)

    def create(self, validated_data):
        print(validated_data)
        return Task.objects.create(**validated_data)

    class Meta:
        model = Task
        fields = ["id", "project", "title", "description", "project", "due_date", "status", "assignees", "version", "created_at", "updated_at"]
        read_only_fields = ["id", "version", "created_at", "updated_at"]
