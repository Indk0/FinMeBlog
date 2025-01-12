from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.admin.views.decorators import staff_member_required
from random import shuffle

# Easter egg response for the index route


def index(request):
    return HttpResponse("This is an easter egg!!!")


# Display a randomized list of published posts
def post_list(request):
    posts = list(Post.objects.filter(status=1))  # Get published posts
    shuffle(posts)  # Randomize order of posts
    return render(request, 'fin_blog/index.html', {'posts': posts})


# View for displaying post details


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)  # Get the post by slug
    comments = post.comments.filter(approved=True).order_by(
        '-created_on')  # Fetch only approved comments
    comment_count = comments.count()  # Count approved comments
    comment_form = CommentForm()  # Empty form for authenticated users

    return render(
        request,
        'fin_blog/post_detail.html',
        {
            'post': post,
            'comments': comments,
            'comment_count': comment_count,
            'comment_form': comment_form,
        },
    )


# Allow logged-in users to create a new post

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'fin_blog/create_post.html', {'form': form})

# Allow logged-in users to add comments to a post


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True).order_by('-created_on')
    comment_count = comments.count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Save comment without committing to DB
            comment = form.save(commit=False)
            comment.post = post   # Link comment to post
            comment.author = request.user  # Set the author
            comment.save()  # Save to the database
            messages.success(
                request,
                "Your comment has been submitted and is awaiting approval.")
            return redirect('post_detail', slug=post.slug)

    else:
        form = CommentForm()

    return render(
        request,
        'fin_blog/post_detail.html',
        {
            'post': post,
            'comment_form': form,
        },
    )

# Allow logged-in users to delete their comments


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(
        Comment, id=comment_id, author=request.user)  # Ensure ownership
    comment.delete()  # Delete the comment
    messages.success(request, "Your comment has been deleted.")
    return redirect('post_detail', slug=comment.post.slug)

# Allow logged-in users to edit their comments


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(
        Comment, id=comment_id, author=request.user)  # Ensure ownership
    if request.method == "POST":
        # Populate form with existing comment
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()  # Save changes
            messages.success(request, "Your comment has been edited.")
            return redirect('post_detail', slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)  # Populate form for GET request
    return render(
        request,
        'fin_blog/edit_comment.html',
        {
            'form': form,
            'comment': comment
        }
    )


# Allow logged-in users to edit their posts
@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)  # Ensure ownership
    if request.method == 'POST':
        # Populate form with existing post
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()  # Save changes
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)  # Populate form for GET request
    return render(request, 'fin_blog/edit_post.html', {'form': form})


# Admin functionality: Approve a category
@staff_member_required
def approve_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.approved = True  # Approve the category
    category.save()
    messages.success(request, f"Category '{category.name}' has been approved.")
    return redirect('admin_category_list')  # Redirect to category list


# Admin functionality: Delete a category
@staff_member_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()  # Delete the category
    messages.success(request, f"Category '{category.name}' has been deleted.")
    return redirect('admin_category_list')  # Redirect to category list


# Admin functionality: List unapproved categories
@staff_member_required
def admin_category_list(request):
    unapproved_categories = Category.objects.filter(
        approved=False)  # Get unapproved categories
    return render(
        request,
        'admin_category_list.html',
        {'unapproved_categories': unapproved_categories})


# Display posts filtered by a specific category
def category_posts(request, slug):
    # Ensure category is approved
    category = get_object_or_404(Category, slug=slug, approved=True)
    posts = category.posts.filter(status=1).order_by(
        '-created_on')  # Get published posts in category
    return render(request, 'fin_blog/category_posts.html', {
        'category': category,
        'posts': posts
    })
