from django.contrib import admin
from django.urls import path

from place.views import CategoryDetailView

app_name='place'

urlpatterns = [
     path('post/<int:pk>', CategoryDetailView.as_view(), name='post'),
]
