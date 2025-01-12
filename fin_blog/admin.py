from django.contrib import admin
from .models import Post, Comment, Category, Reaction
from django_summernote.admin import SummernoteModelAdmin

# Register models here.

# Code for admin to approve or delete user generated categories from CRUD

# Admin configuration for managing user-generated categories


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "approved", "created_at",
                    "updated_at")  # Columns displayed in admin list view
    prepopulated_fields = {"slug": ("name",)}  # Auto-fill slug field from name
    search_fields = ("name",)  # Enable search by category name
    ordering = ["name"]  # Sort categories alphabetically by name
    # Custom actions for bulk operations
    actions = ['approve_categories', 'delete_selected_categories']

    # Action to approve categories
    def approve_categories(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected categories have been approved.")
    # Display name for the action
    approve_categories.short_description = "Approve selected Categories"

# Admin configuration for managing user reactions on posts


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "reaction", "created_at",
                    "updated_at")  # Columns displayed in admin list view
    # Enable search by related fields
    search_fields = ("post__title", "user__username", "reaction")
    # Filter by reaction type and creation date
    list_filter = ("reaction", "created_at")
    ordering = ("-created_at",)  # Sort by newest reactions first

# Code for userpost functionality combined with summernote

# Admin configuration for managing posts with Summernote integration


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = (
        'title', 'author', 'status', 'slug', 'created_on', 'updated_on',
        'featured_image')  # Columns displayed in admin list view
    # Enable search by title, content, or slug
    search_fields = ['title', 'content', 'slug']
    # Filter by status, categories, or creation date
    list_filter = ('status', 'categories', 'created_on')
    # Auto-fill slug field from title
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_on',)  # Sort posts by newest first
    # Enable Summernote editor for content field
    summernote_fields = ('content',)

# Admin configuration for managing comments


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Columns displayed in admin list view
    list_display = ('post', 'author', 'body', 'approved', 'created_on')
    # Filter by approval status and creation date
    list_filter = ('approved', 'created_on')
    # Enable search by comment body or author username
    search_fields = ('body', 'author__username')
    actions = ['approve_comments']  # Custom action for bulk approval

# Action to approve selected comments
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected comments have been approved.")
    # Display name for the action
    approve_comments.short_description = "Approve selected comments"
