from django.urls import path, include
from . import views
from .api import PostResource, UserResource

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<id>/', views.detail, name='detail'),
    path('create_post/', views.create_post, name='create_post'),
    path('posts/<id>/edit', views.edit_post, name='edit'),
    path('posts/<id>/delete', views.delete_post, name='delete'),
    path('posts/<id>/like', views.like_post, name='like'),
    path('posts/<id>/like_index', views.like_post_index, name='like_index'),
    path('api/posts/', include(PostResource.urls())),
    path('api/users/', include(UserResource.urls())),

]