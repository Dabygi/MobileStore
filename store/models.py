from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    """Продукт"""
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField("Название", max_length=255)
    price = models.DecimalField("Цена", max_digits=9, decimal_places=2)
    description = models.TextField("Описание", null=True)
    image = models.ImageField("Изображение", upload_to="images/")
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True                 # абстрактная модель не будет создавать миграций
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Notebook(Product):
    """Ноутбуки"""
    diagonal = models.CharField("Диагональ", max_length=255)
    display_type = models.CharField("Тип дисплея", max_length=100)
    processor_freq = models.CharField("Частота процессора", max_length=100)
    ram = models.CharField("Оперативная память", max_length=100)
    video_card = models.CharField("Видео карта", max_length=255)
    time_without_charge = models.CharField("Время работы от батареи", max_length=100)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    class Meta:
        verbose_name = "Ноутбук"
        verbose_name_plural = "Ноутбуки"

#ноутбуки

# Diagonal
# Display
# Processor_freq
# Ram
# Video
# Time_without_carge


class Smartphone(Product):
    """Ноутбуки"""
    diagonal = models.CharField("Диагональ", max_length=255)
    display_type = models.CharField("Тип дисплея", max_length=100)
    resolution = models.CharField("Разрешение экрана", max_length=100)
    accum_volume = models.CharField("Объем аккумулятора", max_length=100)
    ram = models.CharField("Оперативная память", max_length=100)
    sd = models.BooleanField(default=True)
    sd_volume = models.CharField("Максимальный размер карт памяти", max_length=100)
    main_cam_mp = models.CharField("Основная камера", max_length=100)
    frontal_cam_mp = models.CharField("Фронтальная камера", max_length=100)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    class Meta:
        verbose_name = "Смартфон"
        verbose_name_plural = "Смартфоны"

#смартфоны

# diagonal
# display
# resolution
# accum_volume
# ram
# sd
# sd_volume
# main_cam_mp
# frontal_cam_mp




class CartProduct(models.Model):
    """Продукт в корзине"""
    user = models.ForeignKey('Customer', verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name="Корзина", on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # Покажет все существующие модели в админке
    object_id = models.PositiveIntegerField()                               # Индефицирует категории
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField("Общая цена", max_digits=9, decimal_places=2)

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.title)

    class Meta:
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"


class Cart(models.Model):
    """Корзина"""
    owner = models.ForeignKey('Customer', verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField("Общая цена", max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"


class Customer(models.Model):
    """Пользователь"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField("Номер телефона", max_length=20)
    address = models.CharField("Адрес", max_length=255)

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
