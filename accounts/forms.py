from django import forms
from .models import Comment  # Adjust import based on your app structure


# Form for adding or editing comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Bind to Comment model
        fields = ['body']  # Include only the 'body' field in the form


# Form for adding or editing categories
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category  # Bind to Category model
        # Include 'name' and 'description' fields in the form
        fields = ['name', 'description']
