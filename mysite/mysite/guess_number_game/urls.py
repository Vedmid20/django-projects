from django.urls import path
from .views import index

app_name = 'guess_number_game'

urlpatterns = [
    path('', index, name='home'),
]