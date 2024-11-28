from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'is_admin']  # Include is_admin for assigning roles