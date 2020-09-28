from django.shortcuts import render
from django.views.generic import DetailView

from .models import Notebook, Smartphone


def test_view(request):
    return render(request, 'index.html', {})

class ProductDetailView(DetailView):   # Вывод информации о продукции

    CT_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone,
    }

    def dispatch(self, request, *args, **kwargs):                  # Возможность вывода несколких моделей
        self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'url'