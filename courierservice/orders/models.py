from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()


class CourierProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Пользователь'
    )
    orders = models.ManyToManyField(
        'Order',
        related_name='orders_of_current_courier',
        verbose_name='Заказы',
        blank=True
    )
    image = models.ImageField(
        upload_to='photo_of_couriers/',
        verbose_name='Изображения'
    )


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
    WAITING_SUBMIT = 'WS'
    GOING_TO = 'GT'
    ON_THE_WAY = 'OTW'
    DELIVERED = 'DV'
    STATUS_CHOICES = (
        (WAITING_SUBMIT, 'Waiting submit'),
        (GOING_TO, 'going to'),
        (ON_THE_WAY, 'On the way'),
        (DELIVERED, 'delivered'),
    )
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
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True
    )
    status = models.CharField(
        'Статус заказа',
        max_length=40,
        choices=STATUS_CHOICES,
        default=WAITING_SUBMIT
    )
    comment = models.TextField(
        'Обращение к курьеру',
        max_length=2000,
        blank=True
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


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"


class Rating (models.Model):
    """Рейтинг"""
    star = models.ForeignKey(
        RatingStar,
        verbose_name="звезда",
        on_delete=models.CASCADE
    )
    courier = models.ForeignKey(
        CourierProfile,
        verbose_name='Курьер',
        on_delete=models.CASCADE,
        related_name='rating_of_courier'
    )

    def __str__(self):
        return f'{self.star} - {self.courier.user.name}'

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    text = models.TextField("Отзыв", max_length=5000)
    courier = models.ForeignKey(
        CourierProfile,
        verbose_name="Родитель",
        on_delete=models.SET_NULL,
        null=True
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Отзывы на: {self.courier.user.name}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        default_related_name = 'reviews_of_courier'
