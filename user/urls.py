from django.contrib import admin
from django.urls import path
from user.views import SignupView, LoginView

app_name='user'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
