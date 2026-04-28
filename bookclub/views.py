from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Book
from django.contrib.auth.decorators import login_required




@login_required
def book_home(request):
    curBook = Book.objects.order_by('-month').first()
    reviews = curBook.reviews.all()

    return render(request, "bookclub/bookclubindex.html" , {
        "book" : curBook,
        "reviews" : reviews,
    })



def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'bookclub/signup.html', {'form': form})