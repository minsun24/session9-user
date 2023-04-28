from django.contrib import auth
from django.contrib.auth import authenticate, login, logout 
from .models import CustomUser  
from .models import Profile
from django.shortcuts import render, redirect 
from .forms import CustomUserSigninForm, CustomUserSignupForm   

#form - 유효성 검사 



# 회원가입
def signup(request):
    form = CustomUserSignupForm() #객체 만들어서
    
    #착한 사용자
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)  #사용자의 입력값만 유효한지 판단 
        if form.is_valid():         #유효할 경우
            user = form.save()      #폼데이터를 DB에 저장
            login(request, user)    #장고 제공 login() 
            return redirect("home") #home이라는 이름의 path로 redirect 
            
    #나쁜 사용자
    return render(request, "newSignup.html", {"form": form}) 
    #유효성 검사를 하는 객체도 함께 보내줌 - 유효성 검사 하도록 
    
    
        
    

# 로그인
def signin(request):
    form = CustomUserSigninForm()  #폼 객체 생성
    
    #착한 사용자
    if request.method == "POST":
        form = CustomUserSigninForm(request, request.POST)  #인자 두 개 받아서 확인해야 함!!!  
        if form.is_valid():
            login(request, form.get_user()) #로그인이므로 일치하는지만 확인 save() 필요없음
            return redirect ("home")   
        
    #나쁜 사용자
    return render(request, "newSignin.html", {"form": form})  



# 로그아웃
def signout(request):
    logout(request) 
    return redirect("home") 


def new_profile(request):
    # 로그인하지 않았다면 프로필 누르더라도 계속 홈으로 이동
    if request.user.is_anonymous:
        return redirect("home")
    # 로그인했다면 해당 user의 profile 보기
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'newProfile.html', {"profile":profile})
    # get 한다라는 것은 이미 존재한다 = created = FALSE
    # create 한다라는 것은 존재하지 않는다 = created = TRUE

def create_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.nickname = request.POST.get('nickname')
        profile.image = request.FILES.get('image')
        profile.save()
        return redirect('users:new_profile')

    return render(request, 'newProfile.html', {'profile': profile})

    
    
    
    

# # 회원가입
# def signup(request):
#     if request.method == 'POST':
#         if request.POST['password1'] == request.POST['password2']:
#             user = User.objects.create_user(
#                 username=request.POST['username'],
#                 password=request.POST['password1'],
#                 email=request.POST['email'],)
#             profile = Profile(user=user, nickname=request.POST['nickname'], image=request.FILES.get('profile_image'))
#             profile.save()

#             auth.login(request, user)
#             return redirect('/')
#         return render(request, 'signup.html')
#     return render(request, 'signup.html')

# # 로그인
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')

# # 로그아웃
# def logout(request):
#   auth.logout(request)
#   return redirect('home')