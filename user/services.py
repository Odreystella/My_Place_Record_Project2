from django.contrib.auth.tokens import default_token_generator

from user.dto import ValidTokenDto
from user.models import User

class UserVerificationService:
    token_generator = default_token_generator
    
    def is_valid_token(self, **kwargs):
        user = User.objects.filter(pk=kwargs['pk']).first()
        is_valid = self.token_generator.check_token(user, kwargs['token'])

        if is_valid:               
            # 유효한 토큰인 경우만 is_active를 바꿔줌
            # 악의적으로 url에 난수를 대입할 경우 인증에 실패하는데, 실패한다고 is_active=Flase로 바꾸면 정상적인 사용자의 인증상태가 바뀔 수 있기 때문에 에러 메시지만 띄우는 것이 안전함
            # 인증에 성공할 경우 auth.login()하면 사용자 입장에서는 편리할 수 있으나 보안강도가 약해지는 단점이 있음
            user.is_active = True
            user.save()
        return is_valid


class UserService:
    @staticmethod
    def find_by_user_pk(user_pk):
        return User.objects.filter(pk=user_pk).first()