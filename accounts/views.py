from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def profile(request):
    user_posts = request.user.blog_posts.all()  # Accessing posts
    user_comments = request.user.commenter.all()  # Accessing comments
    return render(request, 'accounts/profile.html', {
        'posts': user_posts,
        'comments': user_comments,
    })
