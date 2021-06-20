from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import CreateView, TemplateView
from django.views import View

from config import settings
from user.forms import UserSignupForm, UserLoginForm
from user.services import UserVerificationService, UserService

# CreateView로 회원가입뷰 생성하기
# TemplateView 와 다르게 model, fields 클래스 변수 추가
class UserSignupView(CreateView):
    model = get_user_model()                      # settings.py에서 AUTH_USER_MODEL이 가르키는 모델을 자동으로 찾아주는 함수
    form_class = UserSignupForm                   # 커스텀한 SignupForm과 연결하기
    success_url = '/user/login/'                  # 가입 완료 후 redirect 해줄 url, index로 redirect
    verify_url = '/user/verify/'
    email_template_name = 'user/verification.html'
    token_generator = default_token_generator     # 사용자 데이터를 가지고 해시데이터를 만들어주는 객체, 이를 이용해 사용자 고유의 토큰을 생성함
    
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

    def send_verification_email(self, user):
        token = self.token_generator.make_token(user)
        url = self.build_verification_link(user, token)
        subject = '회원가입을 축하드립니다.'
        message = '다음 주소로 이동하셔서 인증해주시길 바랍니다. {}'.format(url)  # 일부 이메일 클라이언트에서 html형식의 이메일을 지원하지 않는 경우 보여짐
        html_message = render(self.request, self.email_template_name, {'url':url}).content.decode('utf-8')
        # render함수는 HttpResponse 객체를 반환함
        # 반환한 객체의 content 속성에는 렌더링된 메시지가 저장되어 있는데 http로 전송할 수 있도록 byte로 인코딩 되어 있음
        # 그래서 email_user 메서드의 인자로 전달할 때 utf-8로 디코딩 해줘야 함
        user.email_user(subject, message, settings.EMAIL_HOST_USER, html_message=html_message)
        # user.email_user('회원가입을 축하드립니다.', '다음 주소로 이동하셔서 인증해주시길 바랍니다. {}'.format(self.build_verification_link(user, token)), from_email=settings.EMAIL_HOST_USER)
        messages.info(self.request, '회원가입을 축하드립니다. 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요.')

    def build_verification_link(self, user, token):   # 사용자 인증 페이지의 url을 만들어주는 메소드
        return '{}/user/{}/verify/{}/'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)
    
    # 회원가입 하며 인증메일 보내기
    # - 1. 회원가입 폼 작성 후, 가입버튼 누르면 폼객체의 필드값들의 유효성을 검증하는 로직을 거침
    # - 2. 검증을 통과하면 각 필드의 값을 DB에 저장하고, 폼객체의 instance 변수에 저장함
    # - 3. user/views/py의 UserSignupView의 form_vaild 메서드가 호출됨
    # - 4. form.instance에 저장된 유저객체가 있으면 사용자 email로 인증메일 발송 메서드 호출
    # - 5-1. 토큰 생성, 인증 페이지 url 포함해서 user.email_user 호출하면 settings.EMAIL_HOST_USER가 메일 발송함
    # - 5-2. 인증 페이지 url은 user.pk와 유저 고유의 토큰으로 생성함
    # - 6. 가입한 메일로 인증 메일이 왔는지 확인
    # - 7. 인증 메일 url을 클릭하여 인증하기, url에 user.pk와 token으로 check_token함
    # - 8-1. 정상적인 사용자의 경우 is_active를 True로 바꿔주고 인증에 성공했다는 메시지 띄우고 login페이지로 redirect
    # - 8-2. 비정상적인 사용자의 경우 인증에 실패했다는 메시지 띄우고, login페이지로 redirect
    # - 9. 인증되지 않은 사용자의 경우 인증 이메일 재발송이 가능한 링크 제공  <- 추가 예정

# 사용자 인증뷰 : url의 사용자pk와 토큰을 가지고 해당 사용자의 정상적인 토큰인지 확인되면 인증 여부를 알려줌
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
