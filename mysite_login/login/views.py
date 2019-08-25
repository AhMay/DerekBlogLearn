import hashlib
from django.shortcuts import render, redirect

from .models import User
from .forms import UserForm,RegisterForm
# Create your views here.

def hash_code(s,salt='mysite'):#加点盐
    h = hashlib.sha256()
    s+=salt
    h.update(s.encode()) #update方法只接收bytes类型
    return h.hexdigest()

def index(request):
    pass
    return render(request,'login/index.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = '请检查填写的内容'
       # username = request.POST.get('username',None)
       # password = request.POST.get('password',None)
      #  if username and password:
       #     username = username.strip()
            #用户名字符合法性验证
            #密码长度验证
            #更多的其他验证
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] =user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确"
            except:
                message = "用户名不存在"
        return render(request, 'login/login.html',locals())
    login_form = UserForm()
    return render(request,'login/login.html',locals())

def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/') #登录状态不允许注册

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password2 != password1:
                message="两次输入的密码不同"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user: #用户名已经存在
                    message = "用户名已经存在，请重新选择用户名!"
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = "该邮箱地址已经被注册，请使用别的邮箱！"
                    return render(request, 'login/register.html', locals())
            new_user = User.objects.create()
            new_user.name = username
            new_user.password = hash_code(password1)
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            return redirect('/login/') #跳转到登录页面
    register_form = RegisterForm()
    return render(request,'login/register.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index/')
    request.session.flush() #一次性将session中的所有内容全部清空
    return redirect('/index/')