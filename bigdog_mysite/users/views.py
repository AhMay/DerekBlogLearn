from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import auth
from .forms import RegistrationForm,LoginForm,ProfileForm,PwdChangeForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'] #username validation已经验证了重复用户的问题
            email = form.cleaned_data['email']
            passowrd = form.cleaned_data['password2']
            #使用内置User自带create_user 方法创建用户， 不需要save()
            user = User.objects.create_user(username=username,password=passowrd,email=email)
            #如果直接使用objects.create()方法后不需要使用save()
            user_profile = UserProfile(user=user)
            user_profile.save()
            return redirect('/accounts/login/')
        else:
            message = form.errors
            return render(request, 'users/register.html', {'form': form,
                                                           'message':message})
    else:
        form = RegistrationForm()
    return render(request,'users/register.html',{'form':form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return redirect(reverse('users:profile',args=[user.id]))# 完成后转到用户资料页面 profile页面
            else:
                return render(request, 'users/login.html', {
                    'form': form,
                    'message': 'Wrong password. Please try again.'})
        else:
            message = form.errors
            return render(request, 'users/login.html', {
                'form': form,
                'message': message})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/accounts/login/')

@login_required
def profile(request, pk):
    user =get_object_or_404(User,pk=pk)
    return render(request,'users/profile.html',{'user':user})

@login_required
def profile_update(request, pk):
     #完成后转到profile 页面
    user = get_object_or_404(User,pk=pk)
    form_data = {
         'first_name': user.first_name,
         'last_name': user.last_name,
         'org': user.profile.org,
         'telephone': user.profile.telephone
     }
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            user.profile.org = form.cleaned_data['org']
            user.profile.telephone = form.cleaned_data['telephone']
            user.profile.save()
            return render(request, 'users/profile.html', {'user': user})
        else:
            return render(request, 'users/profile_update.html',{
                'form':form,
                'message':form.errors
            })
    else:
        form = ProfileForm(form_data)
    return render(request,'users/profile_update.html',{
        'form':form
    })

@login_required
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = PwdChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            user = auth.authenticate(username=user.username,password=old_password)
            if user is not None and user.is_active:
                new_password = form.cleaned_data['password1']
                user.set_password(new_password)
                user.save()
                return redirect('/accounts/login/')
        else:
            render(request, "users/pwd_change.html",{'form':form,
                                                     'message':form.errors})
    else:
        form = PwdChangeForm()
    return render(request,"users/pwd_change.html",{'form':form})
