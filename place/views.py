from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import generic

from place.models import Category
from place.services import PlaceService


# class IndexView(TemplateView):
#     template_name = "index.html"

# 카테고리 리스트 보여주는 뷰
class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'index.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['posts'] = PlaceService.get_all_posts()
        return context


# 카테고리 pk로 관련 글의 리스트를 보여주는 뷰
class CategoryDetailView(generic.DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'place_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = PlaceService.find_by_post(self.kwargs['pk'])
        return context