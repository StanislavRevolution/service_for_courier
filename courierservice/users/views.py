from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import UserSignUpForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'authorization/signup_form.html'
    success_url = reverse_lazy('users:login')

