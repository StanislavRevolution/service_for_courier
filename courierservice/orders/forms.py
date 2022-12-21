from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CourierForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Телефон', help_text='+7', required=True)
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea,
        required=True
    )


