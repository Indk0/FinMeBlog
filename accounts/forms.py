from django import forms
from .models import Comment  # Adjust import based on your app structure


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']  # Ensure this matches the model field name
