from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.project_app.models import Project, Task
from apps.core.permissions import admin_permission
from apps.project_app.forms import ProjectForm, TaskForm

@login_required
def projects_view(request):
    projects = Project.objects.get_user_projects(request.user)
    return render(request, "project_list.html", context={"projects": projects})

@login_required
def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.get_tasks_by_project(project_id=project_id)
    return render(request, "project_detail.html", context={"project": project, "tasks": tasks})

@login_required
def create_project_view(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("projects:project-list-page")
    else:
        form = ProjectForm()
    return render(request, "create_project.html", context={"form": form})

@login_required
def create_task_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("projects:project-detail-page", project_id=project_id)
    else:
        form = TaskForm()
    return render(request, "create_task.html", context={"form": form, "project": project})
