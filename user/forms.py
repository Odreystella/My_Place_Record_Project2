from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.forms.fields import EmailField

# UserCreationForm 상속받아서 Form 커스텀하기
class SignupForm(UserCreationForm):

    class Meta:
        model = get_user_model()   # settings.py에서 AUTH_USER_MODEL이 가르키는 모델을 자동으로 찾아주는 함수
        fields = ['email', 'name', 'selfie'] # 정의된 모델에서 폼에 보여줄 필드를 정의함, password는 UserCreationForm에서 자동으로 생성해줌

class LoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus':True})) # 로그인할 때 email 태그의 type이 text -> email
