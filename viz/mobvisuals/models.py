from django.db import models
from django import forms
# Create your models here.

class LoginForms(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=100)
