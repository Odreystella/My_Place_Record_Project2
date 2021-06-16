from django.contrib import admin
from django.urls import path
from user.views import UserSignupView, UserLoginView, UserVerificationView

app_name='user'

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('<pk>/verify/<token>/', UserVerificationView.as_view(), name='verify'),
    path('login/', UserLoginView.as_view(), name='login'),
]
