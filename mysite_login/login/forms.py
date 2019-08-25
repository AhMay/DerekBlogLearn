'''
django 表单 三个主要功能:
 准备和重构数据用于页面渲染
 为数据创建HTML表单元素
 接收和处理用户从表单发过来的数据
'''

from django import forms
from captcha.fields import CaptchaField

class RegisterForm(forms.Form):
    gender = (
        ('mail', '男'),
        ('femail', '女'),
    )
    username = forms.CharField(label='用户名',max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(label='邮箱地址', widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class':'form-control'})) #widge用户指定改字段在form表单里面为密码输入框
    captcha = CaptchaField(label='验证码')