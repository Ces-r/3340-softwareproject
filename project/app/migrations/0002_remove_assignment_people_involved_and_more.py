# Generated by Django 4.2.16 on 2024-12-02 22:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='people_involved',
        ),
        migrations.AddField(
            model_name='assignment',
            name='people_involved',
            field=models.ManyToManyField(related_name='assignments', to=settings.AUTH_USER_MODEL),
        ),
    ]
