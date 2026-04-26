from django.urls import path
from . import views


urlpatterns = [
    path("", views.book_home, name="book_home")
]