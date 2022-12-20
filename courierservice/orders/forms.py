from django import forms


class CourierForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    phone = forms.CharField(label='Телефон', required=True)
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea,
        required=True
    )
