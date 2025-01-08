from django.urls import path
from . import views

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
]
