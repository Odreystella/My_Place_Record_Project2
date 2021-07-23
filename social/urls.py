from django.contrib import admin
from django.urls import path
from .views import CommentCreateView

app_name='social'

urlpatterns = [
    path('comment/', CommentCreateView.as_view(), name='comment'),
]
