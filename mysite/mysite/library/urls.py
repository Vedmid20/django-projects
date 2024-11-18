from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.index, name='home'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
]