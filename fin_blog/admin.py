from django.contrib import admin
from .models import Post, Comment, Category, Reaction

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)

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