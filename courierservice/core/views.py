# core/views.py
from django.shortcuts import render


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию;
    # выводить её в шаблон пользовательской страницы 404 мы не станем
    return render(request, '', {'path': request.path}, status=404)


def csrf_failure(request, reason=''):
    return render(request, '')


def handler500(request):
    return render(request, '', status=500)
