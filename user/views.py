from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

from user.forms import SignupForm
from user.models import User

# CreateView로 회원가입뷰 생성하기
# TemplateView 와 다르게 model, fields 클래스 변수 추가
class SignupView(CreateView):
    model = get_user_model()             
    form_class = SignupForm     # 커스텀한 SignupForm과 연결하기
    success_url = '/'           # 가입 완료 후 redirect 해줄 url
    
    # model = User              # 자동생성 폼에서 사용할 모델, User 모델에 정의된 필드들 사용, model이 정의되면 Form 객체 자동 생성
    # form_class = UserCreationForm # auth가 가지고 있는 폼 사용하기, username이 필수라 커스텀 필요
    # fields = ['email', 'name', 'password']  # 자동생성 폼에서 사용할 필드, 비밀번호 암호화가 안됨
    # template_name_suffix = '_form'
    # template_name = 'user_form.html'