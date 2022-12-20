from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from orders.views import UserSignUpView

app_name = 'users'

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('signup_for_couriers/', UserSignUpView.as_view(), name='signup'),
    path(
        'logout/',
        LogoutView.as_view(template_name='orders/logged_out.html'),
        name='logout'),

    path(
        'login/',
        LoginView.as_view(template_name='orders/login.html'),
        name='login'
    ),
]
