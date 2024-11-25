from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    # Resolve conflicts by overriding related_name for inherited fields
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Unique related_name
        blank=True,
    )

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    people_involved = models.TextField()
