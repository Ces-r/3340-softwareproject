from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True) 
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    people_involved = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assignments')
