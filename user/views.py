from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import CreateView

from config import settings
from user.forms import UserSignupForm, UserLoginForm
from user.models import User

# CreateView로 회원가입뷰 생성하기
# TemplateView 와 다르게 model, fields 클래스 변수 추가
class UserSignupView(CreateView):
    model = get_user_model()             
    form_class = UserSignupForm                   # 커스텀한 SignupForm과 연결하기
    success_url = '/user/login/'              # 가입 완료 후 redirect 해줄 url, index로 redirect
    verify_url = '/user/verify/'
    token_generator = default_token_generator # 사용자 데이터를 가지고 해시데이터를 만들어주는 객체, 이를 이용해 사용자 고유의 토큰을 생성함
    
    # model = User              # 자동생성 폼에서 사용할 모델, User 모델에 정의된 필드들 사용, model이 정의되면 Form 객체 자동 생성
    # form_class = UserCreationForm # auth가 가지고 있는 폼 사용하기, username이 필수라 커스텀 필요
    # fields = ['email', 'name', 'password']  # 자동생성 폼에서 사용할 필드, 비밀번호 암호화가 안됨
    # template_name_suffix = '_form'
    # template_name = 'user_form.html'

    def form_valid(self, form):   # 폼객체의 필드값들이 유효성 검증을 통과할 경우 호출됨, 각 필드의 값을 데이터베이스에 저장하고, 저장된 데이터를 폼객체의 instance 변수에 저장
        response = super().form_valid(form)
        if form.instance:  # user 객체가 있다면
            self.send_verification_email(form.instance)
        return response

    def send_verification_email(self, user):
        token = self.token_generator.make_token(user)
        user.email_user('회원가입을 축하드립니다.', '다음 주소로 이동하셔서 인증해주시길 바랍니다. {}'.format(self.build_verification_link(user, token)), from_email=settings.EMAIL_HOST_USER)
        messages.info(self.request, '회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.')

    def build_verification_link(self, user, token):   # 사용자 인증 페이지의 url을 만들어주는 메소드
        return '{}/user/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)
    
#LoginView로 로그인뷰 생성하기
class UserLoginView(LoginView):
    authentication_form = UserLoginForm  # form_class = LoginForm보다 나은 방법, LoginForm 내부적으로 authentication_form 다음으로 form_class 확인
    template_name = 'user/login_form.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.' )
        return super().form_invalid(form)