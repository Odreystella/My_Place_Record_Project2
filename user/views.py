from django.shortcuts import render, redirect
from django.views.generic import CreateView

from user.models import User

# CreateView로 회원가입뷰 생성하기
# TemplateView 와 다르게 model, fields 클래스 변수 추가
class SignupView(CreateView):
    model = User                            # 자동생성 폼에서 사용할 모델, User 모델에 정의된 필드들 사용, model이 정의되면 Form 객체 자동 생성
    fields = ['email', 'name', 'password']  # 자동생성 폼에서 사용할 필드
    # template_name_suffix = '_form'
    # template_name = 'user_form.html'