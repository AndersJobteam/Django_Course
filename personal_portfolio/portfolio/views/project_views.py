from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ..forms import ProjectCommentForm
from ..models import Project

def projects(request, amount: int = 10):
    search_query = request.GET.get("search_query", "")
    if search_query:
        all_projects = Project.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query)).order_by("-id")[:amount]
    else:
        all_projects = Project.objects.all().order_by("-id")[:amount]
    return render(request, "projects.html", {"projects": all_projects, "search_query": search_query})


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