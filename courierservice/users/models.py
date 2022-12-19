from django.contrib.auth.models import AbstractUser
from django.db import models

from orders.models import Order

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = models.CharField(
        'Никнейм',
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
    bio = models.TextField('Описание', max_length=500, blank=True)
    is_courier = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phoneNumber = PhoneNumberField(
        unique=True,
        null=False,
        blank=False
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class CourierUser(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Пользователь'
    )

    orders = models.ManyToManyField(
        Order,
        related_name='orders_of_current_courier',
        verbose_name='Заказы'
    )
    image = models.ImageField(
        upload_to='photo_of_couriers/',
        verbose_name='Изображения'
    )


