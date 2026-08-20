from django.contrib import admin
from django.db import models as django_models
import inspect
from . import models

for name, obj in inspect.getmembers(models):
    if (
        inspect.isclass(obj)
        and obj.__module__ == models.__name__
        and issubclass(obj, django_models.Model)
    ):
        admin.site.register(obj)