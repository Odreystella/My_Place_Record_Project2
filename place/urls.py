from django.contrib import admin
from django.urls import path

from place.views import CategoryDetailView, PostDetailView

app_name='place'

urlpatterns = [
     path('post/<int:pk>', CategoryDetailView.as_view(), name='post'),
     path('post/detail/<int:pk>', PostDetailView.as_view(), name='detail'),
]
