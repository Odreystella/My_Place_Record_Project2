from django.forms.forms import Form
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import CreateView, TemplateView, FormView, View
# from django.views import View
from django.middleware.csrf import _compare_masked_tokens

from django.conf import settings
from user.forms import UserSignupForm, UserLoginForm, VerificationEmailForm
from user.services import UserVerificationService, UserService
from user.mixins import VerifyEmailMixin
from user.oauth.providers.naver import NaverLoginMixin

# CreateView로 회원가입뷰 생성하기
# TemplateView 와 다르게 model, fields 클래스 변수 추가
class UserSignupView(VerifyEmailMixin, CreateView):
    model = get_user_model()                      # settings.py에서 AUTH_USER_MODEL이 가르키는 모델을 자동으로 찾아주는 함수
    form_class = UserSignupForm                   # 커스텀한 SignupForm과 연결하기
    success_url = '/user/login/'                  # 가입 완료 후 redirect 해줄 url, index로 redirect
    verify_url = '/user/verify/'
    template_name_suffix = '_signupform'          # CreateView는 templates/user/모델명_form.html을 사용하는데 바꾸고 싶으면 template_name = 'signup.html' 하거나 suffix를 수정함

    # model = User                                # 자동생성 폼에서 사용할 모델, User 모델에 정의된 필드들 사용, model이 정의되면 Form 객체 자동 생성
    # form_class = UserCreationForm               # auth가 가지고 있는 폼 사용하기, username이 필수라 커스텀 필요
    # fields = ['email', 'name', 'password']      # 자동생성 폼에서 사용할 필드, 비밀번호 암호화가 안됨
    # template_name_suffix = '_form'
    # template_name = 'user_form.html'

    def form_valid(self, form):   # 폼객체의 필드값들이 유효성 검증을 통과할 경우 호출됨, 각 필드의 값을 데이터베이스에 저장하고, 저장된 데이터를 폼객체의 instance 변수에 저장
        response = super().form_valid(form)
        if form.instance:  # user 객체가 있다면
            self.send_verification_email(form.instance)
        return response

    #### 회원가입 하며 인증메일 보내기 ####
    # 1. 회원가입 폼 작성 후, 가입버튼 누르면 폼객체의 필드값들의 유효성을 검증하는 로직을 거침
    # 2. 검증을 통과하면 각 필드의 값을 DB에 저장하고, 폼객체의 instance 변수에 저장함
    # 3. user/views/py의 UserSignupView의 form_vaild 메서드가 호출됨
    # 4. form.instance에 저장된 유저객체가 있으면 사용자 email로 인증메일 발송 메서드 호출
    # 5-1. 토큰 생성, 인증 페이지 url 포함해서 user.email_user 호출하면 settings.EMAIL_HOST_USER가 메일 발송함
    # 5-2. 인증 페이지 url은 user.pk와 유저 고유의 토큰으로 생성함
    # 6. 가입한 메일로 인증 메일이 왔는지 확인
    # 7. 인증 메일 url을 클릭하여 인증하기, url에 user.pk와 token으로 check_token함
    # 8-1. 정상적인 사용자의 경우 is_active를 True로 바꿔주고 인증에 성공했다는 메시지 띄우고 login페이지로 redirect
    # 8-2. 비정상적인 사용자의 경우 인증에 실패했다는 메시지 띄우고, login페이지로 redirect
    # 9. 인증되지 않은 사용자의 경우 인증 이메일 재발송이 가능한 링크 제공  <- 추가 예정


# 인증 이메일 재발송 뷰 : 폼의 유효성이 검증된 후 인증 이메일을 발송
class ResendVerifyEmailView(VerifyEmailMixin, FormView):
    model = get_user_model()
    form_class = VerificationEmailForm
    success_url = '/user/login/'
    template_name = 'user/resend_verify_email.html'

    def form_valid(self, form):   # 폼객체의 필드값들이 유효성 검증을 통과할 경우 호출됨, 각 필드의 값을 데이터베이스에 저장하고, 저장된 데이터를 폼객체의 instance 변수에 저장
        email = form.cleaned_data['email']  # 폼객체는 유효성검증 작업이 끝나면 cleaned_data라는 인스턴스 변수에 각 필드 이름으로 사용자가 입력한 값들을 저장함
                                            # 사용자가 입력한 이메일을 확인할 수 있음
        try:
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            messages.error(self.request, '알 수 없는 사용자 입니다.')
        else:
            self.send_verification_email(user)
        return super().form_valid(form)


# 사용자 인증뷰 : 인증페이지에서 url의 사용자 pk와 토큰을 가지고 해당 사용자의 정상적인 토큰인지 확인되면 인증 여부를 알려줌
class UserVerificationView(TemplateView):
    model = get_user_model()
    redirect_url = '/user/login/'
    token_generator = default_token_generator  # 토큰의 유효성 확인

    # 데이터 처리 부분은 services에서 하려고 코드 분리
    def get(self, request, *args, **kwargs):
        result = UserVerificationService.is_valid_token(self, **kwargs)
        print(result)
        if result:
            messages.info(request, '인증이 완료되었습니다.')
        else:
            messages.error(request, '인증이 실패하였습니다.')
        return HttpResponseRedirect(self.redirect_url)   # 인증 성공 여부와 상관없이 무조건 로그인 페이지로 redirect


# LoginView로 로그인뷰 생성하기
class UserLoginView(LoginView):
    authentication_form = UserLoginForm  # form_class = LoginForm보다 나은 방법, LoginForm 내부적으로 authentication_form 다음으로 form_class 확인
    template_name = 'user/login_form.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.' )
        return super().form_invalid(form)


# 마이페이지 뷰 생성하기
class MypageView(View):
    def get(self, request, *args, **kwargs):
        user_pk = self.kwargs['pk']
        user = UserService.find_by_user_pk(user_pk)
        context = {'user' : user}
        return render(request, 'user/mypage.html', context)

    def post(self, request, *args, **kwargs):
        pass


# 소셜 로그인뷰, 화면 없고, 서버단에서 네이버 인증토큰을 받고 인증처리하는 기능
class SocialLoginCallBackView(NaverLoginMixin, View):
    success_url = settings.LOGIN_REDIRECT_URL     # index.html로
    failure_url = settings.LOGIN_URL              # login.html로
    required_profiles = ['email', 'name']
    
    model = get_user_model()

    def get(self, request, *args, **kwargs):
        provider = kwargs.get('provider')   # url 라우터로부터 프로바이더 이름을 인자로 받음
        success_url = request.GET.get('next', self.success_url)  # 로그인 하지 않은 상태에서 글 쓰려고 하면 로그인 페이지로 인동하고, next=쿼리가 추가되는데, 소셜로그인 하더라도 게시글 작성 화면으로 이동하게함

        if provider == 'naver':
            csrf_token = request.GET.get('state') 
            # print('token:', csrf_token)
            code = request.GET.get('code')
            if not _compare_masked_tokens(csrf_token, request.COOKIES.get('csrftoken')): # url의 query 값의 state 값(naverLogin()에서 전달한)과 쿠키의 csrftoken을 비교함
                messages.error(request, '잘못된 경로로 로그인하셨습니다.')
                return HttpResponseRedirect(self.failure_url)

            is_success, error = self.login_with_naver(csrf_token, code) # state 값이 정상적인 값이라면 로그인 시도
            
            if not is_success:   # 로그인 실패할 경우
                messages.error(request, error)
            return HttpResponseRedirect(self.success_url if is_success else self.failure_url)
        
        return HttpResponseRedirect(self.failure_url)

    def set_session(self, **kwargs):
        for key, value in kwargs.items():
            self.request.session[key] = value
