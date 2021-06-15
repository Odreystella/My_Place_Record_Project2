from django.contrib import admin
from django.urls import path
from user.views import UserSignupView, UserLoginView

app_name='user'

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
]
