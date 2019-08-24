from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from API import models
from rest_framework.request import Request
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication

from .utils.permission import MyPremission
#from rest_framework.versioning import QueryParameterVersioning
#from rest_framework.versioning import URLPathVersioning

from rest_framework.parsers import JSONParser, FormParser
import json
from .models import Role
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = "__all__"

class GroupView(APIView):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        obj = models.UserGroup.objects.filter(pk=pk).first()

        ser = GroupSerializer(instance=obj,many=False)
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)

'''
class UserInfoSerializer(serializers.Serializer):
    #序列化用户的信息
    type = serializers.CharField(source="get_user_type_display")
    username = serializers.CharField()
    password = serializers.CharField()
    group = serializers.CharField(source="group.title")
    rls = serializers.SerializerMethodField() #然后写一个自定义的方法

    def get_rls(self,row):
        role_obj_list = row.roles.all() #获取用户所有的角色
        ret = []
        for item in role_obj_list: #获取角色的id和名字，以字典的建值对形式显示
            ret.append({"id":item.id,"title": item.title})
        return ret
'''
class UserInfoSerializer(serializers.ModelSerializer):
   # type = serializers.CharField(source="get_user_type_display")
   # group = serializers.CharField(source="group.title")
  #  rls = serializers.SerializerMethodField()
    # def get_rls(self, row):
    #     # 获取用户所有的角色
    #     role_obj_list = row.roles.all()
    #     ret = []
    #     # 获取角色的id和名字
    #     # 以字典的键值对方式显示
    #     for item in role_obj_list:
    #         ret.append({"id": item.id, "title": item.title})
    #     return ret
    group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_field='group_id', lookup_url_kwarg='pk')
    class Meta:
        model = models.UserInfo
        fields = ['id','username','password','group','roles']
        depth = 0 #表示连表的深度

class UserInfoView(APIView):
    '''用户信息'''
    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        # 这里必须要传参数context={'request':request}
        ser = UserInfoSerializer(instance=users,many=True, context={'request':request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        return  HttpResponse(ret)

#要先写一个序列化的类
class RoleSerializer(serializers.Serializer):
    #Role表里面的字段 id 和title 序列化
    id = serializers.IntegerField()
    title = serializers.CharField()

class RolesView(APIView):
   def get(self,request,*args,**kwargs):
       # 方式一：对于[obj,obj,obj]
       # （Queryset）
       # roles = models.Role.objects.all()
       # 序列化，两个参数，instance:Queryset  如果有多个值，就需要加 mangy=True
       # ser = RolesSerializer(instance=roles,many=True)
       # 转成json格式，ensure_ascii=False表示显示中文，默认为True
       # ret = json.dumps(ser.data,ensure_ascii=False)

       # 方式二：
       role = models.Role.objects.all().first()
       ser = RoleSerializer(instance=role, many=False)
       ret = json.dumps(ser.data, ensure_ascii=False)
       return HttpResponse(ret)

class PaserView(APIView):
    parser_classes = [JSONParser, FormParser]
    def post(self, request,*args,**kwargs):
        #获取解析后的结果
        print(request.data)
        return HttpResponse('paser')

class UserView(APIView):
   # versioning_class = QueryParameterVersioning
    #versioning_class = URLPathVersioning
    def get(self, request, *args,**kwargs):
        # 获取版本
        print(request.version)
        # 获取处理版本的对象
        print(request.versioning_scheme)
        # 获取浏览器访问的url，reverse反向解析
        # 需要两个参数：viewname就是url中的别名，request=request是url中要传入的参数
        # (?P<version>[v1|v2]+)/users/，这里本来需要传version的参数，但是version包含在request里面（源码里面可以看到），所有只需要request=request就可以
        url_path = request.versioning_scheme.reverse(viewname='api_user', request=request)
        print(url_path)
        # self.dispatch
        return HttpResponse('用户列表')

ORDER_DICT = {
    1:{
        'name':'apple',
        'price':15
    },
    2:{
        'name':'dog',
        'price':100
    }
}

def md5(user):
    import hashlib
    import time
    #当前时间，相当于生成一个随机的字符串
    ctime = str(time.time())
    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))
    return m.hexdigest()

class AuthView(APIView):
    '''用于用户登录验证'''
    authentication_classes = []    #里面为空，代表不需要认证
    permission_classes = []  #不里面为空，代表不需要权限
    def post(self,request,*args,**kwargs):
        ret = {'code':1000,'msg':None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(username=user,password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            #为用户创建token
            token = md5(user)
            #存在就更新，不存在就创建
            models.UserToken.objects.update_or_create(user=obj,defaults={'token':token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        return JsonResponse(ret)

class OrderView(APIView):
    '''
    订单相关业务
    权限 配置实例 (只有 SVIP用户才能看)
    '''

    def get(self,request,*args,**kwargs):
        # self.dispatch
        #request.user
        #request.auth
        ret = {'code':1000,'msg':None,'data':None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)

'''
class UserInfoView(APIView):
     #  订单相关业务(普通用户和VIP用户可以看)
    permission_classes = [MyPremission,]    #不用全局的权限配置的话，这里就要写自己的局部权限
    def get(self,request,*args,**kwargs):

        print(request.user)
        return HttpResponse('用户信息')
'''