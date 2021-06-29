from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser
from django.db.models.base import Model

# 인증백엔드 코드
# NaverLoginMixin에서 사용, 또한 로그인을 시도할 때 어떤 백엔드를 사용할지에 대해 설정임
# 로그인된 상태에서 또다른 요청을 할 때 장고는 세션의 정보를 확인하여 로그인된 사용자가 맞는지, 맞다면 어떤 사용자인지를 식별하는데 장고의 기본값인 기본인증백엔드를 통해 식별처리함
# 소셜로그인으로 인증할 경우에는 NaverBackend를 사용하게끔 설정 필요

UserModel = get_user_model()


class NaverBackend(ModelBackend):
    def authenticate(self, request, username=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)  # 이메일이 사용자 테이블에 존재하는지
        except UserModel.DoesNotExist:
            pass             # 존재하지 않는다면 none 리턴
        else:
            if self.user_can_authenticate(user):    # 해당메소드는 is_active가 True인지 확인하는 기능
                return user                         # 비밀번호와 관게없으니 인증벡엔드의 인증테스트 종료, 소셜로그인은 이미 프로바이더(네이버)에게 인증을 위임했기 때문에 인증백엔드에서 추가로 인증할게 없음
                                                    # user모델에서 이메일 외에 무언가 추가로 인증해야 할 필드들이 생겼을 경우 여기서 추가인증하면 됨

                                                