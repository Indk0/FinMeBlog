from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Adjust the import based on your Post model's location
from fin_blog.models import Post
# Adjust this based on your Post form's location
from fin_blog.forms import PostForm
# Ensure this matches your Comment model location
from fin_blog.models import Comment
# Ensure this matches your Comment form location
from fin_blog.forms import CommentForm

# Create your views here.


@login_required
def profile(request):
    user_posts = request.user.blog_posts.all()  # Accessing posts
    user_comments = Comment.objects.filter(author=request.user)
    # Accessing comments
    return render(request, 'accounts/profile.html', {
        'posts': user_posts,
        'comments': user_comments,
    })


@login_required
def edit_post(request, post_id):
    # Ensure the user owns the post
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            # Redirect to the profile page after saving
            return redirect('profile')
    else:
        form = PostForm(instance=post)
    return render(request, 'accounts/edit_post.html', {'form': form})


@login_required
def publish_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.status = 1  # Assuming '1' means published
    post.save()
    return redirect('profile')  # Redirect back to the profile page


@login_required
def edit_comment(request, comment_id):
    # Ensure the user owns the comment
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            # Redirect back to the account/profile page after saving
            return redirect('profile')
    else:
        form = CommentForm(instance=comment)
        # Preload the form with the existing comment

    return render(
        request, 
        'accounts/edit_comment.html', {'form': form, 'comment': comment})
