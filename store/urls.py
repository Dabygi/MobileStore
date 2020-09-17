from django.urls import path
from store.views import index

urlpatterns = [
    path('main_page', index),
]