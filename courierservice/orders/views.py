from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView
from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy

from .forms import CourierForm
from users.forms import UserSignUpForm, CourierSignUpForm
from orders.models import CourierProfile

User = get_user_model()


def try_to_send_mail(email):
    try:
        send_mail(
            'Спасибо, что подали заявку на работу в нашей компании',
            'Пройдите регистрацию на курьера по данной ссылке:  '
            'http://127.0.0.1:8000/auth/signup_for_couriers/',
            'courierjob@mail.ru',  # Это поле "От кого"
            [email],  # Это поле "Кому" (можно указать список адресов)
            fail_silently=False,
        )
    except Exception as e:
        return HttpResponse(f'Ошибка при отправке письма: {e}')


@require_http_methods(["GET", "POST"])
def contact_view(request):
    if request.method == 'POST':
        form = CourierForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try_to_send_mail(email)
            return redirect('success/')
    form = CourierForm()
    return render(
        request,
        template_name="orders/applying_for_courier.html",
        context={'form': form}
    )


def success_view(request):
    return HttpResponse('Приняли! Спасибо за вашу заявку.')


def index(request):
    return render(
        request,
        template_name="orders/index.html"
    )


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'orders/signup_form.html'
    success_url = reverse_lazy('orders:index')


class CouriersSignUpView(CreateView):
    model = User
    form_class = CourierSignUpForm
    template_name = 'orders/signup_couriers_form.html'
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'courier'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        valid = super(CouriersSignUpView, self).form_valid(form)
        user = form.save(commit=False)
        user.is_courier = True
        user.save()
        login(self.request, user)
        CourierProfile.objects.create(user=user)
        return valid
