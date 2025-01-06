from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import get_messages


def index(request):
    return HttpResponse("This is an easter egg!!!")

def post_list(request):
    posts = Post.objects.filter(status=1).order_by('-created_on')
    return render(request, 'fin_blog/index.html', {'posts': posts})

# View for displaying post details
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True).order_by('-created_on')  # Fetch only approved comments
    comment_count = comments.count()  # Count approved comments
    comment_form = CommentForm()  # Empty form for authenticated users
   
    return render(request,'fin_blog/post_detail.html', {'post': post,'comments': comments, 'comment_count': comment_count, 'comment_form': comment_form,})

# Create a new post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m() 
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'fin_blog/create_post.html', {'form': form})

# Add a comment to a post
@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True).order_by('-created_on')
    comment_count = comments.count()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Save the comment
            comment = form.save(commit=False)
            comment.post = post  # Set the related post
            comment.author = request.user  # Set the author
            comment.save()  # Save to the database
            messages.success(request, "Your comment has been submitted and is awaiting approval.")
            return redirect('post_detail', slug=post.slug)
        # else:
        #     messages.error(request, "There was an error submitting your comment.")      
    else:
        form = CommentForm()

    return render(request, 'fin_blog/post_detail.html',{'post': post,'comment_form': form,})
