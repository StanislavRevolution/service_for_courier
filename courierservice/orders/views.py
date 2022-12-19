from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import CourierForm


def contact_view(request):
    if request.method == 'GET':
        form = CourierForm()
    elif request.method == 'POST':
        form = CourierForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            try:
                send_mail(
                    'Спасибо, что подали заявку на работу в нашей компании',
                    'Подождите пока с вами свяжется наш менеджер, который'
                    'расскажет о дальнейших действиях.',
                    'courierjob@mail.ru',  # Это поле "От кого"
                    [email],  # Это поле "Кому" (можно указать список адресов)
                    fail_silently=False,
                    # Сообщать об ошибках («молчать ли об ошибках?»)
                )
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect('success')
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, "", {'form': form})


def success_view(request):
    return HttpResponse('Приняли! Спасибо за вашу заявку.')
