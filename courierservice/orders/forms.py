from django import forms
from django.contrib.auth import get_user_model

from orders.models import Order, Product

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
        fields = ('products', 'address', 'comment')
        labels = {
            'products': 'Список продуктов',
            'address': 'Адрес доставки',
            'comment': 'Комментарий для курьера'
        }
        widgets = {
            'products': forms.Select(),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['products'].queryset = Product.objects.none()


