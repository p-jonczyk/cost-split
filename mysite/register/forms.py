from dataclasses import fields
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    # add email field to register form
    email = forms.EmailField()

    # change properties of django form
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
