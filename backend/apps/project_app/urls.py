from django.urls import path
from apps.project_app.apis import (
    ProjectView,
    ProjectDetailView,
    TaskView,
    TaskDetailView,
    ProjectMembershiView,
)
from apps.project_app.views import (
    projects_view,
    project_detail_view,
    create_project_view,
    create_task_view,
)

urlpatterns = [
    # pages
    path("page/", projects_view, name="project-list-page"),
    path("<int:project_id>/page/", project_detail_view, name="project-detail-page"),
    path("create/page/", create_project_view, name="create-project-page"),
    path("<int:project_id>/create-task/", create_task_view, name="create-task-page"),

    # apis
    path("projects/", ProjectView.as_view(), name="project-list"),
    path("projects/<int:project_id>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/<int:project_id>/tasks/", TaskView.as_view(), name="project-task-list"),
    path("projects/<int:project_id>/tasks/<int:task_id>/", TaskDetailView.as_view(), name="task-detail"),
    path("projects/invite/", ProjectMembershiView.as_view(), name="invite-to-project"),
]
