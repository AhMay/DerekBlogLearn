from django.urls import path,re_path
from .views import UserView,PaserView,RolesView,UserInfoView,GroupView,UserGroupView
from .views import Pager1View

urlpatterns = [
    re_path('(?P<version>[v1|v2]+)/users/', UserView.as_view(),name = 'api_user'),  #版本
    path('paser/', PaserView.as_view(),),   #解析
    re_path('(?P<version>[v1|v2]+)/roles/', RolesView.as_view()),     #序列化
    re_path('(?P<version>[v1|v2]+)/info/', UserInfoView.as_view()),   #序列化
    re_path('(?P<version>[v1|v2]+)/group/(?P<pk>\d+)/', GroupView.as_view(),name = 'gp'),    #序列化生成url
    re_path('(?P<version>[v1|v2]+)/usergroup/', UserGroupView.as_view(),),    #序列化做验证
    re_path('(?P<version>[v1|v2]+)/pager1/', Pager1View.as_view(),)    #分页1
]