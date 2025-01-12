from django import forms
from .models import Post, Comment, Category

# Form for creating and editing posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # Bind to Post model
        fields = ['title', 'content', 'status', 'excerpt', 'categories',
                  'featured_image']  # Fields to include in the form
        widgets = {
            # Use checkboxes for selecting categories
            'categories': forms.CheckboxSelectMultiple(),
        }

# Form for adding comments to posts


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Bind to Comment model
        fields = ['body']  # Fields to include in the form
        # Customise field label
        labels = {'body': 'Type your comment in the box below!!'}

# Form for creating and editing categories


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category  # Bind to Category model
        fields = ['name']  # Fields to include in the form
