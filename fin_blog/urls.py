from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
]
