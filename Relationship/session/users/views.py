from django.shortcuts import render
from django.contrib.auth import authenticate  
from django.contrib.auth.models import User  
from .models import Profile   
from django.shortcuts import render, redirect   
from django.contrib import auth   


# TODO: 회원가입
def signup(request):
  #회원가입 요청 post 요청
  if request.method == 'POST':  
    if request.POST['password1'] == request.POST['password2']: #비밀번호 재확인
      user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password1'],
        email=request.POST['email'],
      )
      # 입력받은 회원 정보로 프로필 객체 생성
      profile = Profile(
        user=user,
        nickname=request.POST['nickname'],
        image = request.FILES.get('profile_image')
      )
      profile.save() #프로필 저장
      
      auth.login(request, user) #가입한 회원정보로 로그인
      
      return redirect('/') #홈으로 이동
    
    return render(request, 'signup.html') 
  return render(request, 'signup.html')

# TODO: 로그인
def login(request):
  if request.method=="POST":
    username = request.POST['username']
    password=request.POST['password']
    #존재하는 유저인지 판별
    user = authenticate(request, username=username, password=password) #데이터베이스에 존재하는 유저이면 유저 반환
    
    if user is not None:
      auth.login(request, user)
      return redirect('/')
    return render(request, 'login.html')
  return render(request, 'login.html')  

# TODO: 로그아웃
def logout(request):
  auth.logout(request)
  return redirect('home')