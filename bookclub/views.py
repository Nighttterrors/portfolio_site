from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Book, Profile
from .forms import ReviewForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import user_passes_test




def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def approval_dashboard(request):
    pending_users = Profile.objects.filter(isApproved=False).select_related('user')

    return render(request, "bookclub/approval_dashboard.html", {
        "pending_users": pending_users
    })

@user_passes_test(is_admin)
def approve_user(request, user_id):
    profile = Profile.objects.get(user__id=user_id)
    profile.isApproved = True
    profile.save()

    return redirect("approval_dashboard")






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


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('book_home')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'bookclub/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
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


@login_required
def members(request):
    members = Profile.objects.filter(
        isApproved = True
    ).select_related('user')

    return render(request, 'bookclub/members.html', {
        'members' : members
    })