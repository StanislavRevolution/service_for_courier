from django.core.mail import send_mail
from django.http import HttpResponse


def try_to_send_mail(email):
    try:
        send_mail(
            'Спасибо, что подали заявку на работу в нашей компании',
            'Пройдите регистрацию на курьера по данной ссылке:  '
            'http://127.0.0.1:8000/auth/signup_for_couriers/',
            'courierjob@mail.ru',
            [email],
            fail_silently=False,
        )
    except Exception as e:
        return HttpResponse(f'Ошибка при отправке письма: {e}')