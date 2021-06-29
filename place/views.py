from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import generic, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from config import settings

from place.models import Category, Place
from place.services import PlaceService
from place.dto import CreateDto, UpdateDto


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
class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = settings.LOGIN_URL
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


# 포스트 pk로 해당 포스트 수정하는 뷰
class PostUpdateView(View):
    success_message = '게시글이 수정되었습니다.'

    def get(self, request, *args, **kwargs):
        post_pk = self.kwargs['pk']
        post = PlaceService.get_post(post_pk)
        context = {'post' : post}
        return render(request, 'place_edit.html', context)

    def post(self, request, *args, **kwargs):
        post_pk = self.kwargs['pk']
        post = PlaceService.get_post(post_pk)

        update_dto = self._build_update_dto(request)
        result = PlaceService.update(update_dto)

        if len(messages.get_messages(request)) == 0:
            messages.success(self.request, self.success_message)
        # messages.error(self.request, '알 수 없는 요청입니다.')

        print(result)
        context = {'post' : post, 'error' : result['error']}
        if result['error']['status']:
            return render(request, 'place_edit.html', context)
        return redirect('place:detail', post_pk)

    def _build_update_dto(self, request):
        return UpdateDto(
            name=request.POST['name'],
            location=request.POST['location'],
            stars=request.POST['stars'],
            memo=request.POST['memo'],
            best_menu=request.POST['best_menu'],
            additional_info=request.POST['additional_info'],
            image=request.FILES.getlist('image'),
            pk=self.kwargs['pk']
        )

# 사진 개별 수정하는 뷰 - 미완성
# class PhotoUpdateView(View):
#     success_message = '사진이 수정되었습니다.'

#     def get(self, request, *args, **kwargs):
#         photo = PlaceService.get_photo(self.kwargs['pk'])
#         post = PlaceService.get_post(pthoto_pk)
#         context = {'post' : post}
#         return render(request, 'place_edit.html', context)


#     def post(self, request, *args, **kwargs):
#         photo_pk = self.kwargs['pk']
#         pass

class PostDeleteView(View):
    def get(self, request, *args, **kwargs):
        post_pk = self.kwargs['pk']
        PlaceService.delete(post_pk)

        post = PlaceService.get_post(post_pk)
        category_pk = post.category.pk
        return redirect('place:post', category_pk)