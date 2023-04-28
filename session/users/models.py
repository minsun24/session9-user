from django.db import models
# from django.contrib.auth.models import User #장고가 기본으로 제공해줬던 것 

# 커스텀
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

#django doct 참고 
#커스텀 유저 매니저 (꽌리자)
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs): #**kwargs 키워드 argument, 딕셔너리 형태로 들어감, 받을 인자 개수 정해지지 않음
        user = self.model(username = username,**kwargs)
        user.set_password(password)
        user.save() 
        
    #일반 유저 생성
    def create_normaluser(self, username, password, **kwargs):
        self.create_user(username, password, **kwargs)
    
    
    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault("is_superuser", True)  # 뭔 뜻인지 모르겟음 
        self.create_user(username, password, **kwargs) 
        
        
        
# AbstractBaseUser : 장고가 기본 제공하는 User 모델을 대체하기 위해 사용하는 추상 클래스
# PermissionsMixin : 커스텀한 User 모델에 대한 권한을 부여하기 위해 사용되는 클래스

class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager() #커스텀유저가, 커스텀유저매니저를 사용하겠다. 
    
    USERNAME_FIELD = 'username'  #유저 네임 기준으로 인증하겠다. 
    
    username = models.CharField(unique=True, max_length=20) #요기 username
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    @property   
    def is_staff(self):
        return self.is_superuser 
    

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='profile/', null=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return self.nickname