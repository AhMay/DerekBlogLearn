from django.urls import path,re_path
from .views import UserView, PaserView,RolesView,UserInfoView,GroupView

urlpatterns = [
  #  path('users/',UserView.as_view()),
    re_path('(?P<version>[v1|v2]+)/users/', UserView.as_view(),name='api_user'),
    re_path('group/(?P<pk>\d+)/', GroupView.as_view(),name = 'gp'),     #序列化生成url
    path('paser/',PaserView.as_view(),), #解析
    re_path('(?P<version>[v1|v2]+)/roles/', RolesView.as_view()), #序列化
    re_path('(?P<version>[v1|v2]+)/info/', UserInfoView.as_view()),   #序列化

]