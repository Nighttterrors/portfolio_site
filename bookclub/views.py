from django.shortcuts import render
from .models import Book






def book_home(request):
    curBook = Book.objects.order_by('-month').first()
    reviews = curBook.reviews.all()

    return render(request, "bookclub/bookclubindex.html" , {
        "book" : curBook,
        "reviews" : reviews,
    })
