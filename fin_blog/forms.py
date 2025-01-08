from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'excerpt', 'categories',
                  'featured_image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body': 'Type your comment in the box below!!'}
