import json

from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.versioning import URLPathVersioning
from . import models

##########################################版本和解析器#####################################################

class UserView(APIView):

    def get(self,request,*args,**kwargs):
        #获取版本
        print(request.version)
        #获取处理版本的对象
        print(request.versioning_scheme)
        #获取浏览器访问的url，reverse反向解析
        #需要两个参数：viewname就是url中的别名，request=request是url中要传入的参数
        #(?P<version>[v1|v2]+)/users/，这里本来需要传version的参数，但是version包含在request里面，所有只需要request=request就可以
        url_path = request.versioning_scheme.reverse(viewname='api_user',request=request)
        print(url_path)
        self.dispatch
        return HttpResponse('用户列表')

# from rest_framework.parsers import JSONParser,FormParser

class PaserView(APIView):
    '''解析'''
    # parser_classes = [JSONParser,FormParser,]
    #JSONParser：表示只能解析content-type:application/json的头
    #FormParser:表示只能解析content-type:application/x-www-form-urlencoded的头

    def post(self,request,*args,**kwargs):
        #获取解析后的结果
        print(request.data)
        return HttpResponse('paser')


###########################################序列化###########################################################

from rest_framework import serializers

#要先写一个序列化的类
class RolesSerializer(serializers.Serializer):
    #Role表里面的字段id和title序列化
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
        ser = RolesSerializer(instance=role, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


# class UserInfoSerializer(serializers.Serializer):
#     '''序列化用户的信息'''
#     #user_type是choices（1,2,3），显示全称的方法用source
#     type = serializers.CharField(source="get_user_type_display")
#     username = serializers.CharField()
#     password = serializers.CharField()
#     #group.title：组的名字
#     group = serializers.CharField(source="group.title")
#     #SerializerMethodField(),表示自定义显示
#     #然后写一个自定义的方法
#     rls = serializers.SerializerMethodField()
#
#     def get_rls(self,row):
#         #获取用户所有的角色
#         role_obj_list = row.roles.all()
#         ret = []
#         #获取角色的id和名字
#         #以字典的键值对方式显示
#         for item in role_obj_list:
#             ret.append({"id":item.id,"title":item.title})
#         return ret


# class UserInfoSerializer(serializers.ModelSerializer):
#     type = serializers.CharField(source="get_user_type_display")
#     group = serializers.CharField(source="group.title")
#     rls = serializers.SerializerMethodField()
#
#     def get_rls(self, row):
#         # 获取用户所有的角色
#         role_obj_list = row.roles.all()
#         ret = []
#         # 获取角色的id和名字
#         # 以字典的键值对方式显示
#         for item in role_obj_list:
#             ret.append({"id": item.id, "title": item.title})
#         return ret
#
#     class Meta:
#         model = models.UserInfo
#         fields = ['id','username','password','type','group','rls']

# class UserInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.UserInfo
#         #fields = "__all__"
#         fields = ['id','username','password','group','roles']
#         #表示连表的深度
#         depth = 1


class UserInfoSerializer(serializers.ModelSerializer):
    group = serializers.HyperlinkedIdentityField(view_name='gp',lookup_field='group_id',lookup_url_kwarg='pk')
    class Meta:
        model = models.UserInfo
        #fields = "__all__"
        fields = ['id','username','password','group','roles']
        #表示连表的深度
        depth = 0


class UserInfoView(APIView):
    '''用户的信息'''
    def get(self,request,*args,**kwargs):
        users = models.UserInfo.objects.all()
        #这里必须要传参数context={'request':request}
        ser = UserInfoSerializer(instance=users,many=True,context={'request':request})
        ret = json.dumps(ser.data,ensure_ascii=False)
        return HttpResponse(ret)


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



####################################序列化之用户请求数据验证验证####################################

#自定义验证规则
class GroupValidation(object):
    def __init__(self,base):
        self.base = base

    def __call__(self, value):
        if not value.startswith(self.base):
            message = "标题必须以%s为开头"%self.base
            raise serializers.ValidationError(message)


class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(validators=[GroupValidation('以我开头'),])

class UserGroupView(APIView):
    def post(self,request,*args, **kwargs):
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data['title'])
        else:
            print(ser.errors)

        return HttpResponse("用户提交数据验证")


##################################################分页###################################################

from API.utils.serializsers import PagerSerialiser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

# #自定义分页类1
# class MyPageNumberPagination(PageNumberPagination):
#     #每页显示多少个
#     page_size = 3
#     #默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
#     page_size_query_param = "size"
#     #最大页数不超过10
#     max_page_size = 10
#     #获取页码数的
#     page_query_param = "page"

#自定义分页类2
class MyLimitOffsetPagination(LimitOffsetPagination):
    #默认显示的个数
    default_limit = 2
    #当前的位置
    offset_query_param = "offset"
    #通过limit改变默认显示的个数
    limit_query_param = "limit"
    #一页最多显示的个数
    max_limit = 10


#自定义分页类3 (加密分页)
class MyCursorPagination(CursorPagination):
    cursor_query_param = "cursor"
    page_size = 2     #每页显示2个数据
    ordering = 'id'   #排序
    page_size_query_param = None
    max_page_size = None


class Pager1View(APIView):
    def get(self,request,*args,**kwargs):
        #获取所有数据
        roles = models.Role.objects.all()
        #创建分页对象
        pg = MyCursorPagination()
        #获取分页的数据
        page_roles = pg.paginate_queryset(queryset=roles,request=request,view=self)
        #对数据进行序列化
        ser = PagerSerialiser(instance=page_roles,many=True)
        return Response(ser.data)
        # return pg.get_paginated_response(ser.data)