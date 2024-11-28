from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

    # Add related_name to resolve conflicts with reverse accessors
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True) 
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    people_involved = models.TextField()
