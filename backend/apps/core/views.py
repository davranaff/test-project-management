from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.exceptions import APIException
from apps.core.forms import LoginForm, CustomUserCreationForm
from django.contrib.auth import login


class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "The task was updated by someone else; please refresh."
    default_code = "conflict"


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect("projects:project-list-page")
    else:
        form = LoginForm()
    return render(request, "login.html", context={"form": form})

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("projects:project-list-page")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})
