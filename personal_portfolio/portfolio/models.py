from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to="portfolio/images/")
    url = models.URLField(blank=True)
    pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ProjectComment(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="project_comments",
    )
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        author = self.user.username if self.user else "Former user"
        return f"{author} on {self.project.title}"