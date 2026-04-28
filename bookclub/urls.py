from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.book_home, name="book_home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/' , views.sign_up, name='signup'),
]