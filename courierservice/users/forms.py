from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth import get_user_model

from orders.models import CourierProfile

User = get_user_model()


# class CreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'email')
#
#
# class CourierCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'email')


class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'phoneNumber'
        )


class CourierSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'phoneNumber'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_courier = True
        if commit:
            user.save()
            CourierProfile.objects.create(user=user)
        return user
