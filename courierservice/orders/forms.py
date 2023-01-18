from django import forms
from django.contrib.auth import get_user_model

from orders.models import Order, Reviews

User = get_user_model()


class CourierForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Телефон', help_text='+7', required=True)
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea,
        required=True
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('address', 'comment')
        labels = {
            'address': 'Адрес доставки',
            'comment': 'Комментарий для курьера'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('text', )
