from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('orders:product_list_by_category',
                       args=[self.slug])


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
    bio = models.TextField('Описание', max_length=500, blank=True)
    success_orders = models.PositiveIntegerField(
        'Выполненные заказы',
        blank=True,
        null=True,
        default=0
    )

    class Meta:
        verbose_name = 'Профиль курьера'
        verbose_name_plural = 'Профили курьера'

    def __str__(self):
        return f'Курьер: {self.user.username}'


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('orders:product_detail',
                       args=[self.id, self.slug])


class Order(models.Model):
    WAITING_SUBMIT = 'WS'
    GOING_TO = 'GT'
    ON_THE_WAY = 'OTW'
    DELIVERED = 'DV'
    STATUS_CHOICES = (
        (WAITING_SUBMIT, 'Waiting submit'),
        (GOING_TO, 'Going to'),
        (ON_THE_WAY, 'On the way'),
        (DELIVERED, 'delivered'),
    )
    address = models.CharField(
        'Адрес получателя',
        max_length=400
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Заказчик',
        related_name='all_orders'
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
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.id} of {self.client.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


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
        return f'Отзывы на: {self.courier.user}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        default_related_name = 'reviews_of_courier'
