from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from ..models import Category, Smartphone, Notebook, Customer
from .serializers import (
    CategorySerializer,
    SmartphoneSerializer,
    NotebookSerializer,
    CustomerSerializer,
)


class CategoryPagination(PageNumberPagination):
    """Пагинация"""
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):  # переопределил стандартный вывод
        return Response(OrderedDict([
            ('objects_count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('items', data)
        ]))


class CategoryListAPIView(ListAPIView):
    """API категорий"""
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
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
