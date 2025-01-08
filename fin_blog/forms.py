from django import forms
from .models import Post, Comment, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'excerpt', 'categories',
                  'featured_image']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body': 'Type your comment in the box below!!'}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
