from django.shortcuts import render


def index(request):
    return render(request, 'learn_english/index.html')