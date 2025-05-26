from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'

    books = Book.objects.all()
    books_dict = [{'name': b.name, 'author': b.author, 'pub_date': b.pub_date} for b in books]
    print(books_dict)
    context = {'content': books_dict}
    return render(request, template, context)
