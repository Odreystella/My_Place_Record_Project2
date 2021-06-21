from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.fields import EmailField

from user.validators import RegisteredEmailValidator

# UserCreationForm 상속받아서 Form 커스텀하기
class UserSignupForm(UserCreationForm):

    class Meta:
        model = get_user_model()   # settings.py에서 AUTH_USER_MODEL이 가르키는 모델을 자동으로 찾아주는 함수
        fields = ['email', 'name', 'selfie'] # 정의된 모델에서 폼에 보여줄 필드를 정의함, password는 UserCreationForm에서 자동으로 생성해줌

# 로그인 폼
class UserLoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus':True})) # 로그인할 때 email 태그의 type이 text -> email


# 인증 이메일 재발송 폼
# 이미 인증된 이메일이나, 가입된 적 없는 이메일이 입력된 경우 에러를 발생시키는 유효성 검증필터 추가
# default_validators : 폼의 필드의 유효성을 검증함, 리스트의 각 원소들을 입력된 값을 전달하여 함수처럼 호출함
# validators=(EmailField.default_validators + [RegisteredEmailValidator()]) 의 내부 동작은
# for validator in default_valitors:
#     validator(email)
class VerificationEmailForm(forms.Form):
    email = EmailField(widget=forms.EmailInput(attrs={'autofocus' : True}), validators=(EmailField.default_validators + [RegisteredEmailValidator()]))