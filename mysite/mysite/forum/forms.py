from django import forms
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class AccountForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']