from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):             # Model-View-Template
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:
    """Вывод нескольких продуктов на страницу"""

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')         # если хотим выводить приоритетные модели первыми
        products = []                                           # финальный список товаров
        ct_models = ContentType.objects.filter(model__in=args)  # запрос
        for ct_model in ct_models:                              # итерируясь вызовем свойства модели
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:6]
            products.extend(model_products)                     # соберём модели в список
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products                                         # вернём список 6-и выводимых моделей


class LatestProducts:

    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Смартфоны': 'smartphone__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data



class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    """Продукт"""
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField("Название", max_length=255)
    price = models.DecimalField("Цена", max_digits=9, decimal_places=2)
    description = models.TextField("Описание", null=True)
    image = models.ImageField("Изображение", upload_to="images/")
    slug = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True                 # абстрактная модель не будет создавать миграций
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def get_model_name(self):
        return self.__class__.__name__.lower()


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

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):
    """Смартфоны"""
    diagonal = models.CharField("Диагональ", max_length=255)
    display_type = models.CharField("Тип дисплея", max_length=100)
    resolution = models.CharField("Разрешение экрана", max_length=100)
    accum_volume = models.CharField("Объем аккумулятора", max_length=100)
    ram = models.CharField("Оперативная память", max_length=100)
    sd = models.BooleanField("Наличие SD карты", default=True)
    sd_volume = models.CharField("Максимальный размер карт памяти", max_length=255, null=True, blank=True)
    main_cam_mp = models.CharField("Основная камера", max_length=100)
    frontal_cam_mp = models.CharField("Фронтальная камера", max_length=100)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    class Meta:
        verbose_name = "Смартфон"
        verbose_name_plural = "Смартфоны"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):
    """Продукт в корзине"""
    user = models.ForeignKey('Customer', verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name="Корзина", on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # Покажет все существующие модели в админке
    object_id = models.PositiveIntegerField()                               # Идентифицирует категории
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField("Общая цена", max_digits=9, decimal_places=2)

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.content_object.title)

    class Meta:
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Корзина"""
    owner = models.ForeignKey('Customer', null=True, verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField("Общая цена", max_digits=9, default=0, decimal_places=2)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def save(self, *args, **kwargs):
        cart_data = self.products.aggregate(models.Sum('final_price'), models.Count('id'))
        if cart_data.get('final_price__sum'):
            self.final_price = cart_data['final_price__sum']
        else:
            self.final_price = 0
        self.total_price = cart_data['id__count']
        super().save(*args, **kwargs)


class Customer(models.Model):
    """Пользователь"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="Адрес", null=True, blank=True)

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



