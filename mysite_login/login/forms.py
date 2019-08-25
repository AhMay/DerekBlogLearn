'''
django 表单 三个主要功能:
 准备和重构数据用于页面渲染
 为数据创建HTML表单元素
 接收和处理用户从表单发过来的数据
'''

from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128)
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput) #widge用户指定改字段在form表单里面为密码输入框
