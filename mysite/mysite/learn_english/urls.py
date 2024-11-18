from django.urls import path
from .views import index, about, vocabulary, reading, grammar

app_name = 'learn_english'

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('vacabulary/', vocabulary, name='vocabulary'),
    path('reading/', reading, name='reading'),
    path('grammar/', grammar, name='grammar'),
]