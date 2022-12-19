from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('courier-form/', views.courier_form, name='courier_form'),
    path('courier-form/success/', views.success_view, name='success'),
]
