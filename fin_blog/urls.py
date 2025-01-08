from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/',
         views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/',
         views.delete_comment, name='delete_comment'),
    path('categories/<int:category_id>/approve/',
         views.approve_category, name='approve_category'),
    path('categories/<int:category_id>/delete/',
         views.delete_category, name='delete_category'),
    path('admin/categories/', views.admin_category_list,
         name='admin_category_list'),
]
