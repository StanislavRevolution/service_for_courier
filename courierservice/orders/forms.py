from django import forms
from django.contrib.auth import get_user_model

from users.models import CustomUser


class CourierForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Телефон', required=True)
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea,
        required=True
    )
