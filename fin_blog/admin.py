from django.contrib import admin
from .models import Post, Comment, Category, Reaction
from django_summernote.admin import SummernoteModelAdmin

# Register models here.
# Code for author functionality


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ["name"]


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "reaction", "created_at", "updated_at")
    search_fields = ("post__title", "user__username", "reaction")
    list_filter = ("reaction", "created_at")
    ordering = ("-created_at",)

# Code for userpost functionality combined with summernote


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = (
        'title', 'author', 'status', 'slug', 'created_on', 'updated_on')
    search_fields = ['title', 'content', 'slug']
    list_filter = ('status', 'categories', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_on',)
    summernote_fields = ('content',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'body', 'approved', 'created_on')
    list_filter = ('approved', 'created_on')
    search_fields = ('body', 'author__username')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected comments have been approved.")
    approve_comments.short_description = "Approve selected comments"
