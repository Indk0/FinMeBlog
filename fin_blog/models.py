from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

# Status choices for post publication
STATUS = ((0, "Draft"), (1, "Published"))

# Tracks user reactions (like/dislike) to posts


class Reaction(models.Model):
    post = models.ForeignKey(
        'fin_blog.Post', on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reactions")
    reaction = models.BooleanField()  # True for Like, False for Dislike
    created_at = models.DateTimeField(
        auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for updates

    class Meta:
        # Prevent duplicate reactions per post-user pair
        unique_together = ('post', 'user')

    def __str__(self): return (
        f"{self.user.username} "
        f"{'Liked' if self.reaction else 'Disliked'} "
        f"{self.post.title}"
    )


# Represents categories for organizing posts
class Category(models.Model):
    # Unique category name
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True,
                            blank=True)  # Auto-generated slug
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)  # Category creator
    # Approval status for category
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for updates
    pending_deletion = models.BooleanField(
        default=False)  # Mark category for deletion

    class Meta:
        ordering = ["name"]  # Sort categories alphabetically by name
        verbose_name_plural = "Categories"  # Correct plural for admin display

    def save(self, *args, **kwargs):
        # Auto-generate a unique slug if not provided
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Ensure unique slugs by appending a counter if needed
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Represents individual blog posts
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)  # Unique post title
    slug = models.SlugField(max_length=200, unique=True,
                            blank=True)  # Auto-generated slug
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )  # Post author
    content = models.TextField()  # Main content of the post
    excerpt = models.TextField(blank=True)  # Optional short summary
    # Post status: draft or published
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(
        auto_now_add=True)  # Timestamp for creation
    updated_on = models.DateTimeField(auto_now=True)  # Timestamp for updates
    categories = models.ManyToManyField(
        "Category", related_name="posts")  # Associated categories

    featured_image = CloudinaryField(
        'image',
        default='default_rolq52'
        # Cloudinary public ID for the default image
    )

    def save(self, *args, **kwargs):
        # Auto-generate a slug from the title if not providedif not self.slug:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} | written by {self.author}"

    class Meta:
        ordering = ["-created_on"]  # Sort posts by most recent first


# Represents comments made on posts
class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )  # Associated post
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter"
    )  # Comment author
    body = models.TextField()  # Main content of the comment
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment {self.body} by {self.author}"

    class Meta:
        ordering = ["created_on"]  # Sort comments by creation time
