from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# 에러메시지를 필드에 표시하기 위해 뷰가 아닌 필드에서 유효성 검증하기
# 필드의 유효성 검증 필터는 반드시 __call__ 메소드를 오버라이드 해줘야함
# __call__ : 인스턴스를 invoke 연산자(소괄호)로 호출시 실행하는 함수 Ex)RegisteredEmailValidator()
# 원래 클래스의 인스턴스는 invoke 연산자로 호출이 불가능함, 파이썬에서는 함수도 객체인데, __call__ 메소드가 구현되어 있다고 생각하면 됨
class RegisteredEmailValidator:
    user_model = get_user_model()
    code = 'Invalid'

    def __call__(self, email):
        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            raise ValidationError('가입되지 않은 이메일입니다.', code=self.code)
        else:
            if user.is_active:
                raise ValidationError('이미 인증되어 있습니다.', code=self.code)

        return