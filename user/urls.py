from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from user.views import UserSignupView, UserLoginView, SocialLoginCallBackView, UserVerificationView, ResendVerifyEmailView, MypageView

app_name='user'

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('<pk>/verify/<token>/', UserVerificationView.as_view(), name='verify'),
    path('resend/verify_email/', ResendVerifyEmailView.as_view(), name='re-verify'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('login/social/<provider>/callback/', SocialLoginCallBackView.as_view(), name='social-login-naver' ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mypage/<pk>', MypageView.as_view(), name='mypage'),
]
