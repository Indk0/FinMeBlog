from django.contrib import admin
from .models import Post, Comment, Category

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}   
    search_fields = ("name",)   
    ordering = ["name"]   