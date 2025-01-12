from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from fin_blog.models import Post
from fin_blog.forms import PostForm
from fin_blog.models import Comment
from fin_blog.forms import CommentForm
from fin_blog.models import Category
from fin_blog.forms import CategoryForm
from django.urls import reverse


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
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            if post.status == 0:
                messages.success(request, f"Draft post '{
                                 post.title}' has been updated successfully!")
            else:
                messages.success(request, f"Published post '{
                                 post.title}' has been updated successfully!")
            return redirect('profile')
    else:
        form = PostForm(instance=post)

    return render(
        request, 'accounts/edit_post.html', {'form': form, 'post': post})


@login_required
def publish_post(request, post_id):
    """
    View to publish a draft post.
    """
    post = get_object_or_404(Post, id=post_id, author=request.user)

    # Check if the post is currently a draft
    if post.status == 0:
        post.status = 1  # Change the status to 'published'
        post.save()
        messages.success(request, f"Draft post '{
                         post.title}' has been published successfully!")
    else:
        messages.info(request, f"The post '{
                      post.title}' is already published.")

    return redirect('profile')  # Redirect to the profile page


@login_required
def edit_comment(request, comment_id):
    # Ensure the user owns the comment
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(
                request, "The comment has been successfully edited.")
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
    return render(
        request,
        'accounts/category_list.html', {'categories': categories})


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
    category = get_object_or_404(Category, id=category_id, author=request.user)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            updated_category = form.save(commit=False)

            if not request.user.is_staff:
                updated_category.approved = False
                messages.info(
                    request,
                    "Your edits have been submitted for admin approval.")
            else:
                messages.success(request, f"Category '{updated_category.name}\
                    ' has been updated successfully!")
            updated_category.save()
            return redirect('profile')
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        'accounts/edit_category.html', {'form': form, 'category': category})


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        if request.user.is_staff:  # Admin can delete directly
            category.delete()
            messages.success(request, "Category deleted successfully.")
        else:
            category.pending_deletion = True
            category.approved = False
            category.save()
            messages.info(
                request,
                "Your deletion request has been submitted for admin approval.")
        return redirect('profile')
    return render(
        request,
        'accounts/delete_category.html', {'category': category})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "The comment has been successfully deleted.")
        return redirect('profile')  # Redirect to the profile page
    return render(
        request, 'accounts/delete_comment.html', {'comment': comment})


@login_required
def delete_post(request, post_id):
    """
    View to delete a post (draft or published).
    """
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        is_draft = post.status == 0  # Check if the post is a draft
        deleted_post_title = post.title  # Store the title for feedback
        post_id = post.id  # Store post ID
        post.delete()

        if is_draft:
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Draft post '{deleted_post_title}' deleted successfully!",
                extra_tags=f"draft_{post_id}"
            )
        else:
            messages.success(request, f"Published post '{
                             deleted_post_title}' deleted successfully!")
        return redirect('profile')

    return render(request, 'accounts/delete_post.html', {'post': post})
