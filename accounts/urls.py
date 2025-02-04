from django.urls import path
from . import views
from fin_blog.views import create_post


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/publish/',
         views.publish_post, name='publish_post'),
    path('comment/<int:comment_id>/edit/',
         views.edit_comment, name='edit_comment'),
    path('categories/', views.category_list, name='category_list'),
    path('create_category/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/edit/',
         views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/',
         views.delete_category, name='delete_category'),
    path('create_post/', create_post, name='create_post'),
    path('delete-comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
]
