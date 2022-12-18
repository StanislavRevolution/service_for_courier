from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()


class Product(models.Model):
    title = models.CharField(
        'Название продукта',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=15
    )
    price = models.PositiveSmallIntegerField(
        'Стоимость продукта',
        default=1,
        validators=[
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'measurement_unit'),
                name='unique_title_measurement_unit'
            )
        ]

    def __str__(self):
        return f'{self.title}:{self.measurement_unit}'


class Order(models.Model):
    products = models.ManyToManyField(
        Product,
        through='ProductAmount',
        related_name='products_in_order',
        verbose_name='Продукты'
    )
    address = models.CharField(
        'Адрес получателя',
        max_length=400
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Заказчик'
    )
    courier = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True
    )


class ProductAmount(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Количество'
    )

    class Meta:
        default_related_name = 'product_ammount'
        verbose_name_plural = 'Продукт-Заказ'
        constraints = [
            models.UniqueConstraint(
                fields=('product', 'order'),
                name='unique_product_order'
            ),
            models.CheckConstraint(
                check=models.Q(amount__gte=1),
                name='amount_gte_1'
            )
        ]

    def __str__(self):
        return f'{self.product.title}: {self.amount}'


