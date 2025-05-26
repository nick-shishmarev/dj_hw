from datetime import datetime as dt

from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    books_dict = [{'name': b.name, 'author': b.author, 'pub_date': b.pub_date} for b in books]
    context = {'books': books_dict}
    return render(request, template, context)


def books_view_date(request, pub_date):
    template = 'books/books_list_date.html'

    if pub_date:
        pub_date = dt.strptime(pub_date, "%Y-%m-%d").date()

    books = list(Book.objects.all())
    books.sort(key=lambda b: b.pub_date)
    date_previous = None
    date_next = None
    books_dict = []

    for book in books:
        if book.pub_date < pub_date:
            date_previous = f"{book.pub_date:%Y-%m-%d}"
        elif book.pub_date == pub_date:
            books_dict.append({
                'name': book.name,
                'author': book.author,
                'pub_date': book.pub_date
            })
        else:
            date_next = f"{book.pub_date:%Y-%m-%d}"
            break

    context = {'books': books_dict, 'date_previous': date_previous, 'date_next': date_next, 'date_pub': pub_date}
    return render(request, template, context)
