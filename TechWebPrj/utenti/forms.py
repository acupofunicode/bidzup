from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django import forms
from .views import *

class CreaCompratoreForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        group = Group.objects.get(name="Compratori")
        group.user_set.add(user)
        return user

class CreaVenditoreForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')

