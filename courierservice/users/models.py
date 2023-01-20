from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        db_index=True,
        max_length=255,
        unique=True
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        db_index=True,
        unique=True
    )
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    is_courier = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phoneNumber = PhoneNumberField(
        unique=True,
        null=False,
        blank=False,
        verbose_name='Номер телефона',
        help_text='+7'
    )
    birthday = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return f'/own_profile/{self.id}/'

    def age(self):
        import datetime
        return int((datetime.date.today() - self.birthday).days / 365.25)
