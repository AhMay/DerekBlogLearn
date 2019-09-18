from django.shortcuts import render, HttpResponse,redirect, reverse
from  django.contrib.auth import authenticate, login
from  django.views.generic.base import View
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm,UserinfoForm
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email

import os
import json

class UserInfoView(View):
    def get(self,request):
        return render(request, 'users/usercenter-info.html')

    def post(self, request):
        userinfoform = UserinfoForm(request.POST, instance=request.user)
        if userinfoform.is_valid():
            userinfoform.save()
            print('---here---')
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            print('---line---herhe')
            return HttpResponse(json.dumps(userinfoform.errors), content_type='application/json')

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
    return  render(request,"users/usercenter-info.html")

class UpdatePwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        print(request.POST.get('password1','1'))
        print(request.POST.get('password2', '2'))
        if modify_form.is_valid():
            print("---here---")
            pwd1 = modify_form.cleaned_data['password1']
            pwd2 = modify_form.cleaned_data['password2']
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',  content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

class UploadImageView(View):
    def post(self, request):
        imge_form = UploadImageForm(request.POST, request.FILES)
        if imge_form.is_valid():
            image = imge_form.cleaned_data['image']
            print(request.user.image.url)
            default = os.path.join('users/avatar','default.jpg')
            if not (request.user.image == default):
                os.remove(os.path.join('media','users','avatar',request.user.username,os.path.basename(request.user.image.url)))
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class SendEmailCodeView(View):
    '''发送邮箱修改验证码'''
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send_register_email(email,'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')

class UpdateEmailView(View):
    '''修改邮箱'''
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')
        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}',content_type='application/json')

def logout(request):
    return HttpResponse("logout")

class ActiveUserView(View):
    '''激活用户'''
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'users/active_fail.html')

        login_form = LoginForm()
        return redirect(reverse('login'),{'login_form':login_form})

class RegisterView(View):
    '''用户注册'''
    def get(self, request):
        register_form = RegisterForm()
        return  render(request, 'users/register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data['email']
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'users/register.html', {'register_form':register_form,'msg':'该用户已经存在'})
            pass_word = register_form.cleaned_data['password']
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False #默认用户添加是 True,设为false是为了激活使用
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name, 'register')
            login_form = LoginForm()
            return redirect(reverse('users:login'),{'login_form':login_form})
        else:#form is invalid
            return render(request, 'users/register.html', {'register_form':register_form})

class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'users/login.html',{'login_form': login_form})

    def post(self,request):
        # 获取用户提交的用户名和密码
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            pass_word = login_form.cleaned_data['password']
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # 登录
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    #非激活用户，不能登录
                    return render(request, 'users/login.html', {'msg':'当前用户还没有被激活', 'login_form': login_form})
            else:
                return render(request, 'users/login.html', {'msg': '用户名或密码错误','login_form': login_form})
        else: # form.invalid
            return render(request, 'users/login.html', {'login_form': login_form}) #login_form.errors.items

class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'users/forgetpwd.html', {'forget_form':forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = forget_form.cleaned_data['email']
            send_register_email(email,'forget')
            return render(request, 'users/send_success.html')
        else:
            render(request, 'users/forgetpwd.html', {'forget_form':forget_form})

class ResetView(View):
    def get(self, request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "users/password_reset.html", {"email": email})
        else:
            return render(request, "users/active_fail.html")

        login_form = LoginForm()
        return redirect(reverse('users:login'),{'login_form':login_form})

class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get('email', "")
        if modify_form.is_valid():
            pwd1 = modify_form.cleaned_data['password1']
            pwd2 = modify_form.cleaned_data['password2']
            if pwd1 != pwd2:
                return render(request,'users/password_reset.html', {'email': email, "msg":"密码不一样"})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            login_form = LoginForm()
            return redirect(reverse('users:login'),{'login_form':login_form})
        else:
            return render(request, 'users/password_reset.html', {'modify_form': modify_form,'email': email,})
