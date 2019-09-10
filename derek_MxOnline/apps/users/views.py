from django.shortcuts import render, HttpResponse
from  django.contrib.auth import authenticate, login

from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q

#邮箱和用户名都可以登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 唯一用户，用get
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # django 密码后台加密，所以不能用password == password
            if user.check_password(password):
                return user
        except Exception as e:
            return  None

# Create your views here.

def user_info(request):
    return  HttpResponse("user info")

def logout(request):
    return HttpResponse("logout")

def user_login(request):
    if request.method == 'POST':
        #获取用户提交的用户名和密码
        user_name = request.POST.get('username', None)
        pass_word = request.POST.get('password', None)

        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            #登录
            login(request,user)
            return  render(request, 'index.html')
        else:
            return render(request, 'login.html', {'msg':'用户名或密码错误'})
    elif request.method == 'GET':
        return render(request, 'login.html')

def register(request):
    return HttpResponse("register")

def forget_pwd(request):
    return HttpResponse("forget_pwd")
