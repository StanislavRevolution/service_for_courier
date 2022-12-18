from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'logout/',
        LogoutView.as_view(template_name=''),
        name='logout'),
    path('signup/', views.SignUp.as_view(), name=''),
    path(
        'login/',
        LoginView.as_view(template_name=''),
        name='login'
    ),
   ]
