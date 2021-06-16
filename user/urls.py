from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from user.views import UserSignupView, UserLoginView, UserVerificationView

app_name='user'

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('<pk>/verify/<token>/', UserVerificationView.as_view(), name='verify'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
