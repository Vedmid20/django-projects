from django.urls import path
from .views import index, log_in, create_comment, change_comment, create_account, profile, delete_comment

app_name = 'forum'

urlpatterns = [
    path('', index, name='home'),
    path('log_in/', log_in, name='login'),
    path('create_comment/', create_comment, name='create_comment'),
    path('change_comment/<int:comment_id>/', change_comment, name='change_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('create_account/', create_account, name='create_account'),
    path('profile/', profile, name='profile'),
]
