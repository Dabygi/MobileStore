from rest_framework import serializers

from ..models import Category, Smartphone, Notebook, Customer, Order


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер от модели Категории"""

    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug'
        ]


class BaseProductSerializer:
    """Сериалайзер от базовой модели Продукта"""

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)
    title = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=9, decimal_places=2, required=True)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=True)
    slug = serializers.SlugField(required=True)


class SmartphoneSerializer(BaseProductSerializer, serializers.ModelSerializer):
    """Сериалайзер от модели Смартфонов"""

    diagonal = serializers.CharField(required=True)
    display_type = serializers.CharField(required=True)
    resolution = serializers.CharField(required=True)
    accum_volume = serializers.CharField(required=True)
    ram = serializers.CharField(required=True)
    sd = serializers.BooleanField(required=True)
    sd_volume = serializers.CharField(required=False)
    main_cam_mp = serializers.CharField(required=True)
    frontal_cam_mp = serializers.CharField(required=True)

    class Meta:
        model = Smartphone
        fields = '__all__'


class NotebookSerializer(BaseProductSerializer, serializers.ModelSerializer):
    """Сериалайзер от модели Ноутбуков"""

    diagonal = serializers.CharField(required=True)
    display_type = serializers.CharField(required=True)
    processor_freq = serializers.CharField(required=True)
    ram = serializers.CharField(required=True)
    video_card = serializers.CharField(required=True)
    time_without_charge = serializers.CharField(required=True)

    class Meta:
        model = Notebook
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """Сериалайзер от модели Заказа"""

    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    """Сериалайзер от модели Покупателя"""

    order = OrderSerializer(many=True)   # подробная инфа о заказе

    class Meta:
        model = Customer
        fields = '__all__'