from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.book_home, name="book_home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/' , views.sign_up, name='signup'),
    # path('login/', auth_views.LoginView.as_view(template_name='bookclub/login.html'), name='login'),
]
