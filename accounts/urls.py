from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/publish/', 
         views.publish_post, name='publish_post'),
    path('comment/<int:comment_id>/edit/',
         views.edit_comment, name='edit_comment'),

]
