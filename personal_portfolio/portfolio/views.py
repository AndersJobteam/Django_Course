from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required

from .forms import ProjectCommentForm, SignUpForm, StyledAuthenticationForm
from .models import Project

def home(request):
    projects = Project.objects.filter(pinned=True).order_by("-id")[:2]
    return render(request, 'home.html', {'projects': projects})


def projects(request):
    all_projects = Project.objects.all().order_by("-id")
    return render(request, "projects.html", {"projects": all_projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"/accounts/?next=/projects/{project.pk}/")
        form = ProjectCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
            return redirect("project-detail", pk=project.pk)
    else:
        form = ProjectCommentForm()

    return render(
        request,
        "project_detail.html",
        {"project": project, "comments": project.comments.all(), "form": form},
    )

@login_required
def delete_comment(request, project_pk, comment_pk):
    project = get_object_or_404(Project, pk=project_pk)
    comment = get_object_or_404(
        project.comments,
        pk=comment_pk,
        user=request.user,
    )
    comment.delete()
    return redirect("project-detail", pk=project.pk)

def account(request):
    action = request.POST.get("action", request.GET.get("action", "login"))
    next_url = request.GET.get("next", request.POST.get("next", "/"))
    if not url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
        next_url = "/"

    if request.user.is_authenticated:
        return redirect(next_url)

    if action == "signup":
        form = SignUpForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
        login_form = StyledAuthenticationForm()
    else:
        login_form = StyledAuthenticationForm(request, request.POST or None)
        form = SignUpForm()
        if request.method == "POST" and login_form.is_valid():
            login(request, login_form.get_user())
            return redirect(next_url)

    return render(
        request,
        "account.html",
        {"login_form": login_form, "signup_form": form, "action": action, "next": next_url},
    )

@login_required
def account_logout(request):
    if request.method == "POST":
        logout(request)
    return redirect("home")