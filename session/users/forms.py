from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  #장고에서 제공해주는 form


from .models import CustomUser

#회원가입 시 유효성 검사
class CustomUserSignupForm(UserCreationForm):
  class Meta:
    model = CustomUser
    fields = ['username']
    
#로그인 시 유효성 검사
class CustomUserSigninForm(AuthenticationForm):
  class Meta:
    model = CustomUser
    fields = ['username']
    