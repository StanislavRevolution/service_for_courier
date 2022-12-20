from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import CourierForm
from users.forms import UserSignUpForm
from users.models import CustomUser

User = get_user_model()


def try_to_send_mail(email):
    try:
        send_mail(
            'Спасибо, что подали заявку на работу в нашей компании',
            'Подождите пока с вами свяжется наш менеджер, который '
            'расскажет о дальнейших действиях.',
            'courierjob@mail.ru',  # Это поле "От кого"
            [email],  # Это поле "Кому" (можно указать список адресов)
            fail_silently=False,
            # Сообщать об ошибках («молчать ли об ошибках?»)
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
        template_name="orders/ApplicationForCouriers.html",
        context={'form': form}
    )


def success_view(request):
    return HttpResponse('Приняли! Спасибо за вашу заявку.')


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'orders/signup_form.html'
    success_url = reverse_lazy('orders:index')


def index(request):
    return render(
        request,
        template_name="orders/index.html"
    )
