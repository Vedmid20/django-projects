from django.shortcuts import render
from .models import Word, Category


def index(request):
    return render(request, 'learn_english/index.html')


def about(request):
    return render(request, 'learn_english/about.html')


def vocabulary(request):
    categories = Category.objects.all()
    words_by_category = {category: Word.objects.filter(category=category) for category in categories}
    return render(request, 'learn_english/vocabulary.html', {'words_by_category': words_by_category})


def reading(request):
    return render(request, 'learn_english/reading.html')


def grammar(request):
    return render(request, 'learn_english/grammar.html')