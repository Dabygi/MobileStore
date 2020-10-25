# Generated by Django 3.1.1 on 2020-09-20 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_products', models.PositiveIntegerField(default=0)),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Общая цена')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Категория')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Smartphone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Изображение')),
                ('url', models.SlugField(max_length=130, unique=True)),
                ('diagonal', models.CharField(max_length=255, verbose_name='Диагональ')),
                ('display_type', models.CharField(max_length=100, verbose_name='Тип дисплея')),
                ('resolution', models.CharField(max_length=100, verbose_name='Разрешение экрана')),
                ('accum_volume', models.CharField(max_length=100, verbose_name='Объем аккумулятора')),
                ('ram', models.CharField(max_length=100, verbose_name='Оперативная память')),
                ('sd', models.BooleanField(default=True)),
                ('sd_volume', models.CharField(max_length=100, verbose_name='Максимальный размер карт памяти')),
                ('main_cam_mp', models.CharField(max_length=100, verbose_name='Основная камера')),
                ('frontal_cam_mp', models.CharField(max_length=100, verbose_name='Фронтальная камера')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Смартфон',
                'verbose_name_plural': 'Смартфоны',
            },
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Изображение')),
                ('url', models.SlugField(max_length=130, unique=True)),
                ('diagonal', models.CharField(max_length=255, verbose_name='Диагональ')),
                ('display_type', models.CharField(max_length=100, verbose_name='Тип дисплея')),
                ('processor_freq', models.CharField(max_length=100, verbose_name='Частота процессора')),
                ('ram', models.CharField(max_length=100, verbose_name='Оперативная память')),
                ('video_card', models.CharField(max_length=255, verbose_name='Видео карта')),
                ('time_without_charge', models.CharField(max_length=100, verbose_name='Время работы от батареи')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Ноутбук',
                'verbose_name_plural': 'Ноутбуки',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('qty', models.PositiveIntegerField(default=1)),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Общая цена')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='store.cart', verbose_name='Корзина')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Продукт в корзине',
                'verbose_name_plural': 'Продукты в корзине',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customer', verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_cart', to='store.CartProduct'),
        ),
    ]
