from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import generic

from place.models import Category
from place.services import PlaceService


# class IndexView(TemplateView):
#     template_name = "index.html"

class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'index.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['posts'] = PlaceService.get_all_posts()
        return context
