"""

The `ApprovedManager` class defines a custom manager for Django models
that filters and returns only approved topics or posts.

"""
from django.db import models


class ApprovedManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(approved=True)
        return qs
