from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import generic, View

from place.models import Category, Place
from place.services import PlaceService
from place.dto import CreateDto


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


# 포스트 pk로 해당 포스트 상세내용 보여주는 뷰
class PostDetailView(generic.DetailView):
    model = Place
    context_object_name = 'post'
    template_name = 'place_detail.html'


# 카테고리 pk로 해당 카테고리에 글 생성하는 뷰
class PostCreateView(View):
    def get(self, request, *args, **kwargs):
        category_pk = self.kwargs['pk']
        category = PlaceService.find_by_category(category_pk)
        context = {'category' : category}
        return render(request, 'place_add.html', context)

    def post(self, request, *args, **kwargs):
        category_pk = self.kwargs['pk']
        create_dto = self._build_create_dto(request)
        result = PlaceService.create(create_dto)
        context = { 'error' : result['error']}
        if result['error']['status']:
            return render(request, 'place_add.html', context)
        return redirect('place:post', category_pk)

    def _build_create_dto(self, request):
        category = PlaceService.find_by_category(self.kwargs['pk'])
        return CreateDto(
            category=category,
            author=request.user,
            name=request.POST['name'],
            location=request.POST['location'],
            memo=request.POST['memo'],
            best_menu=request.POST['best_menu'],
            additional_info=request.POST['additional_info'],
            stars=request.POST['stars'],
            # tag=request.POST['tag'],
            image=request.FILES.getlist('image'),
            pk=self.kwargs['pk'],
        )