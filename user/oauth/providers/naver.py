from django.conf import settings
from django.contrib.auth import login

import requests


# 싱글턴 디자인 패턴: 첫번째 생성자 호출 때맨 객체 생성, 이후 생성자 호출부터는 먼저 생성된 객체를 공유하는 방식
# NaverClient 객체는 인스턴스변수가 없기 때문에 하나의 객체를 공유하더라도 문제가 발생하지 않음
# 여러 클래스에서 유틸리티처럼 사용하는 클래스의 경우 싱글턴 패턴을 많이 사용함
# 객체를 생성하는 비용이 줄어 서버의 가용성을 높이는 좋은 패턴임
# 일반적으로 싱글턴은 생성자가 아니라 명시적으로 getInstance라는 static method를 제공해서 객체를 생성
# getInstance를 사용하지 않고 생성자를 사용해 객체를 생성하면 에러를 발생시켜 싱글턴으로 구현되어 있음을 개발자에게 알려줌
# 싱글턴 객체에 인스턴스변수를 추가하거나 클래스 변수를 변경하면 안됨!!!
class NaverClient():
    client_id = settings.NAVER_CLIENT_ID
    secret_key = settings.NAVER_SECRET_KEY
    grant_type = 'authorization_code'

    auth_url = 'https://nid.naver.com/oauth2.0/token'
    profile_url = 'https://openapi.naver.com/v1/nid/me'

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):   
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_access_token(self, state, code):
        res = requests.get(self.auth_url, params={'client_id' : self.client_id, 'client_secret' : self.secret_key,
                                                   'grant_type' : self.grant_type, 'state' : state, 'code' : code })
        print(res.json())
        return res.ok, res.json()

    def get_profile(self, access_token, token_type='Bearer'):
        res = requests.get(self.profile_url, headers={'Authorization' : '{} {}'.format(token_type, access_token)}).json()

        if res.get('resultcode') != '00':
            return False, res.get('message')
        else:
            return True, res.get('response')


class NaverLoginMixin:
    naver_client = NaverClient()    # 네이버의 api 구현, 네이버의 인증토큰 발급과 프로필 정보 가져옴

    def login_with_naver(self, state, code):
    
        # 인증토큰 발급
        # login_with_naver 메소드는 naver_client로부터 token_infos 객체를 전달받음
        is_success, token_infos = self.naver_client.get_access_token(state, code)

        if not is_success:
            return False, '{} [{}]'.format(token_infos.get('error_desc'), token_infos.get('error'))

        # token_infos는 아래와 같은 키를 갖는 딕셔너리 객체임
        # error - 에러코드, error_description - 에러메시지도 있음, 인증토큰을 받아오는데 실패한다면 에러메시지와 함께 함수 종료
        access_token = token_infos.get('access_token')    # 인증토큰
        refresh_token = token_infos.get('refresh_token')  # 인증토큰 재발급 토큰
        expires_in = token_infos.get('expires_in')        # 인증토큰 만료기한(초)
        token_type = token_infos.get('token_type')        # 인증토큰 사용하는 api 호출시 인증방식(Authorization 헤더 타입)

        # 회원가입 진행을 위해 네이버 프로필 얻기 
        is_success, profiles = self.get_naver_profile(access_token, token_type)
        if not is_success:
            return False, profiles

        # 사용자 생성 또는 업데이트
        user, created = self.model.objects.get_or_create(email=profiles.get('email'))
        if created:      # 유저 생성했다면 랜덤한 비밀번호로 설정, 소셜로그인은 로컬 비밀번호 필요 없음
            user.set_password(None)
        user.name = profiles.get('name')   # 기존 회원이라면 user에 get한 user 담김
        user.is_active = True
        user.save()

        # auth 프레임워크의 login함수로 로그인
        # 기본 인증모듈인 django.contrib.auth.backends.ModelBackend는 username(email)과 비밀번호를 이용해 인증처리, 소셜로그인은 비밀번호를 받을 수 없어서 따로 구현해야 함
        login(self.request, user, 'user.oauth.backends.NaverBackend')  # NaverBackend를 통한 인증 시도

        # 소셜로그인의 마지막은 매번 재로그인을 할 수 없으니 세션정보에 인증토큰 정보를 추가하는 것
        self.set_session(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in, token_type=token_type)
        return True, user

    # 인증토큰이 정상적으로 발급되었다면 profile api를 통해 사용자의 이메일과 이름을 받아서 회원가입 시킴
    def get_naver_profile(self, access_token, token_type):
       is_success, profiles = self.naver_client.get_profile(access_token, token_type)
       
       if not is_success:
           return False, profiles

       for profile in self.required_profiles:
            if profile not in profiles:
                return False, '{}은 필수정보입니다. 정보 제공에 동의해주세요.'.format(profile)

       return True, profiles 

