from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Book, Profile, DiscussionPost, PostLike
from .forms import ReviewForm, UserUpdateForm, ProfileUpdateForm, BookForm, DiscussionPostForm, ReplyForm, DiscussionPost, Book, Review
from django.contrib.auth.decorators import user_passes_test
from collections import defaultdict
from django.contrib.auth import authenticate, login




def is_admin(user):
    return user.is_staff

def landing_page(request):
    current_book = Book.objects.filter(
        is_current = True
    ).first()

    return render(request, 'bookclub/landing.html', {
        'book' : current_book
    })


@user_passes_test(is_admin)
def approval_dashboard(request):

    pending_users = Profile.objects.filter(isApproved=False).select_related('user')
    approved_users = Profile.objects.filter(isApproved=True).select_related('user')

    if request.method == 'POST':
        book_form = BookForm(
            request.POST,
            request.FILES
        )

        if book_form.is_valid():
            book_form.save()
            return redirect('approval_dashboard')
    else:
        book_form = BookForm()



    return render(request, "bookclub/approval_dashboard.html", {
        "pending_users": pending_users,
        'approved_users': approved_users,
        'book_form' : book_form,
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
    
    
    curBook = Book.objects.filter(is_current=True).first()
    if not curBook:
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
            return redirect('/books/?login=1')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('/books/?signup=1')       
    return redirect('landing_page')


@login_required
def members(request):
    members = Profile.objects.filter(
        isApproved = True
    ).select_related('user')

    return render(request, 'bookclub/members.html', {
        'members' : members
    })




@login_required
def timeline(request):
    books = Book.objects.order_by('-month')

    grouped_books = defaultdict(list)

    for book in books:
        year = book.month.year
        grouped_books[year].append(book)

    return render(request, 'bookclub/timeline.html', {
        'grouped_books': dict(grouped_books)
    })


@user_passes_test(is_admin)
def delete_member(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Prevent deleting yourself
    if user == request.user:
        return redirect('approval_dashboard')

    user.delete()

    return redirect('approval_dashboard')



@login_required
def forum(request):

    current_book = Book.objects.filter(
        is_current=True
    ).first()

    if not current_book:
        return render(request, 'bookclub/forum.html', {
            'error': 'No current book selected.'
        })

    posts = (
        DiscussionPost.objects
        .filter(book=current_book)
        .select_related('user')
        .prefetch_related(
            'likes',
            'replies',
            'replies__user'
        )
        .order_by('-created_at')
    )
    for post in posts:
        post.user_has_liked = (
            post.likes.filter(
                user=request.user
            ).exists()
        )
    form = DiscussionPostForm()
    reply_form = ReplyForm()
    if request.method == 'POST':

        # REPLY SUBMISSION
        if 'reply_content' in request.POST:

            post_id = request.POST.get(
                'post_id'
            )

            parent_post = DiscussionPost.objects.get(
                id=post_id
            )

            reply_form = ReplyForm({
                'content':
                    request.POST.get(
                        'reply_content'
                    )
            })

            if reply_form.is_valid():

                reply = reply_form.save(
                    commit=False
                )

                reply.user = request.user

                reply.post = parent_post

                reply.save()

            return redirect('forum')


        # NEW DISCUSSION POST
        form = DiscussionPostForm(
            request.POST
        )

        if form.is_valid():

            post = form.save(
                commit=False
            )

            post.user = request.user

            post.book = current_book

            post.save()

            return redirect('forum')
    
    return render(request, 'bookclub/forum.html', {
        'reply_form': reply_form,
        'book': current_book,
        'posts': posts,
        'form': form,
    })


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(
        DiscussionPost,
        id= post_id
    )


    existing_like = PostLike.objects.filter(
        post = post,
        user = request.user
    ).first()

    if existing_like:
        existing_like.delete()

    else:
        PostLike.objects.create(
            post = post,
            user = request.user
        )
    
    return redirect('forum')





def custom_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('book_home')

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect('/books/?login=1')

    return redirect('landing_page')


@login_required
def book_archive(request, book_id):

    book = get_object_or_404(
        Book,
        id=book_id
    )

    reviews = (
        Review.objects
        .filter(book=book)
        .select_related('user')
        .order_by('-created_at')
    )

    posts = (
        DiscussionPost.objects
        .filter(book=book)
        .select_related('user')
        .prefetch_related(
            'likes',
            'replies',
            'replies__user'
        )
        .order_by('-created_at')
    )

    return render(
        request,
        'bookclub/book_archive.html',
        {
            'book': book,
            'reviews': reviews,
            'posts': posts,
        }
    )