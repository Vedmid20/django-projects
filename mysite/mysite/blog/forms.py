from django.forms import ModelForm, Form
from .models import CommentForBlogPost
from django import forms


class CommentForBlogPostForm(ModelForm):
    class Meta:
        model = CommentForBlogPost
        fields = ['text']


class EmailForm(Form):
    subject = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    to = forms.EmailField()