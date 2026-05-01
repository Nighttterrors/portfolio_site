from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Book, Profile
from .forms import ReviewForm



@login_required
def book_home(request):
    #Get or create profile to avoid crashes
    profile, _ = Profile.objects.get_or_create(user=request.user)
    #Gate Access
    if not profile.isApproved:
        return render(request, "bookclub/pending.html")
    
    
    curBook = Book.objects.order_by('-month').first() 
    reviews = curBook.reviews.all() if curBook else []
    
    #Check if the user has already reviewed the book
    existingReview =  None
    if curBook:
        existingReview = curBook.reviews.filter(user=request.user).first()

    form = ReviewForm()

    if request.method == "POST" and curBook:
        form = ReviewForm(request.POST)
        if form.is_valid():
            if existingReview:
                messages.error(request, "You have already submitted a review! 👌")
                return redirect("book_home")
            review = form.save(commit=False)
            review.user = request.user
            review.book = curBook

            try:
                review.save()
                messages.success(request, "Review Submitted")
            except IntegrityError:
                messages.error(request, "You already reviewed this book.")

            return redirect("book_home")

    return render(request, "bookclub/bookclubindex.html" , {
        "book" : curBook,
        "reviews" : reviews,
        "form" : form,
        "existingReview" : existingReview
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