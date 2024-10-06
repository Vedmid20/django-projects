from django.urls import path
from .views import index

app_name = 'learn_english'

urlpatterns = [
    path('', index, name='home'),
]