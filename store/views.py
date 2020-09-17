from django.shortcuts import render
from django.http import HttpResponse

from store.models import Notebook


def index(request):
    return HttpResponse(Notebook.objects.all())
