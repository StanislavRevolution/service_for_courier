from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from orders import views
from users.views import UserSignUpView

app_name = 'users'

urlpatterns = [
    path('courier/<int:pk>/update/', views.CourierUpdateView.as_view(),
         name='update_for_couriers'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('signup_for_couriers/', views.CouriersSignUpView.as_view(),
         name='signup_for_couriers'),
    path(
        'logout/',
        LogoutView.as_view(template_name='authorization/logged_out.html'),
        name='logout'),

    path(
        'login/',
        LoginView.as_view(template_name='authorization/login.html'),
        name='login'
    ),
]
