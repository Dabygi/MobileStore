from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from ..models import Category, Smartphone, Notebook, Customer
from .serializers import (
    CategorySerializer,
    SmartphoneSerializer,
    NotebookSerializer,
    CustomerSerializer,
)


class CategoryListAPIView(ListAPIView):
    """API категорий"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SmartphoneListAPIView(ListAPIView):
    """API смартфонов"""
    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']

class NotebookListAPIView(ListAPIView):
    """API ноутбуков"""
    serializer_class = NotebookSerializer
    queryset = Notebook.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']

class SmartphoneDetailAPIView(RetrieveAPIView):
    """API смартфона по id"""
    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    lookup_field = 'id'

class NotebookDetailAPIView(RetrieveAPIView):
    """API ноутбука по id"""
    serializer_class = NotebookSerializer
    queryset = Notebook.objects.all()
    lookup_field = 'id'

class CustomersListAPIView(ListAPIView):
    """API покупателей"""
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
