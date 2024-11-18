from django.shortcuts import render
from .models import Author, Book
from django.views.generic import DetailView


def index(request):
    authors = Author.objects.all()
    books = Book.objects.all()
    return render(request, 'library/index.html', context={'authors': authors, 'books': books})


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'library/books.html'
    context_object_name = 'author'