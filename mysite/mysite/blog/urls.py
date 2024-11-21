from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('posts/', BlogListView.as_view(), name='posts'),
    path('my-posts/', (UserBlogListView.as_view()), name='my-posts'),
    path('create_post/', BlogCreateView.as_view(), name='create-post'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='post'),
    path('update_post/<slug:slug>/', BlogUpdateView.as_view(), name='update-post'),
    path('delete_post/<slug:slug>/', BlogDeleteView.as_view(), name='delete-post'),
    path('update_comment/<slug:slug>/', CommentUpdateView.as_view(), name='update-comment'),
    path('delete_comment/<slug:slug>/', CommentDeleteView.as_view(), name='delete-comment'),
    path('share_post/<slug:slug>', share_post, name='share-post')
]
