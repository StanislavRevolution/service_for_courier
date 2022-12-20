# Generated by Django 3.2.16 on 2022-12-19 23:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourierProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.customuser', verbose_name='Пользователь')),
                ('image', models.ImageField(upload_to='photo_of_couriers/', verbose_name='Изображения')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=400, verbose_name='Адрес получателя')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')),
                ('status', models.CharField(choices=[('WS', 'Waiting submit'), ('GT', 'going to'), ('OTW', 'On the way'), ('DV', 'delivered')], default='WS', max_length=40, verbose_name='Статус заказа')),
                ('comment', models.TextField(blank=True, max_length=2000, verbose_name='Обращение к курьеру')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название продукта')),
                ('measurement_unit', models.CharField(max_length=15, verbose_name='Единица измерения')),
                ('price', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Стоимость продукта')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Звезда рейтинга',
                'verbose_name_plural': 'Звезды рейтинга',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=5000, verbose_name='Отзыв')),
                ('courier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews_of_courier', to='orders.courierprofile', verbose_name='Родитель')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_of_courier', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'default_related_name': 'reviews_of_courier',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_of_courier', to='orders.courierprofile', verbose_name='Курьер')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.ratingstar', verbose_name='звезда')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='ProductAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_ammount', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_ammount', to='orders.product')),
            ],
            options={
                'verbose_name_plural': 'Продукт-Заказ',
                'default_related_name': 'product_ammount',
            },
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('title', 'measurement_unit'), name='unique_title_measurement_unit'),
        ),
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Заказчик'),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='products_in_order', through='orders.ProductAmount', to='orders.Product', verbose_name='Продукты'),
        ),
        migrations.AddField(
            model_name='courierprofile',
            name='orders',
            field=models.ManyToManyField(blank=True, related_name='orders_of_current_courier', to='orders.Order', verbose_name='Заказы'),
        ),
        migrations.AddConstraint(
            model_name='productamount',
            constraint=models.UniqueConstraint(fields=('product', 'order'), name='unique_product_order'),
        ),
        migrations.AddConstraint(
            model_name='productamount',
            constraint=models.CheckConstraint(check=models.Q(('amount__gte', 1)), name='amount_gte_1'),
        ),
    ]