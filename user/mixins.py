from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render

from config import settings

class VerifyEmailMixin:
    email_template_name = 'user/verification.html'
    token_generator = default_token_generator     # 사용자 데이터를 가지고 해시데이터를 만들어주는 객체, 이를 이용해 사용자 고유의 토큰을 생성함

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
 