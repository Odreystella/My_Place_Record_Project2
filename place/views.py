from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import generic

class IndexView(TemplateView):
    template_name = "index.html"

class CategoryListView(generic.ListView):
    pass