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
from fin_blog.models import Category
from fin_blog.forms import CategoryForm
from django.contrib import messages

# Create your views here.


@login_required
def profile(request):
    user_posts = request.user.blog_posts.all()  # Accessing posts
    user_comments = Comment.objects.filter(
        author=request.user)  # Accessing comments
    user_categories = Category.objects.filter(
        author=request.user)  # Include all categories

    return render(request, 'accounts/profile.html', {
        'posts': user_posts,
        'comments': user_comments,
        'categories': user_categories,  # Pass all categories to the template
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


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'accounts/category_list.html', {'categories': categories})


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.author = request.user
            category.save()
            messages.success(
                request, "Your category has been submitted for approval.")
            # Redirect to profile page after creating
            return redirect('profile')
    else:
        form = CategoryForm()

    return render(request, 'accounts/create_category.html', {'form': form})


@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'accounts/edit_category.html', {'form': form, 'category': category})


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'accounts/delete_category.html', {'category': category})
