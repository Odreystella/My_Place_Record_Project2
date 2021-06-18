from django.contrib import admin
from django.urls import path

from place.views import CategoryDetailView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name='place'

urlpatterns = [
     path('post/<int:pk>', CategoryDetailView.as_view(), name='post'),
     path('post/detail/<int:pk>', PostDetailView.as_view(), name='detail'),
     path('post/add/<int:pk>', PostCreateView.as_view(), name='add'),
     path('post/edit/<int:pk>', PostUpdateView.as_view(), name='edit'),
     # path('photo/edit/<int:pk>', PhotoUpdateView.as_view(), name='photo-edit'),
     path('post/delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
]
