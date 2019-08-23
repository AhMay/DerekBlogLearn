from django.urls import path,re_path
from .views import UserView, PaserView,RolesView

urlpatterns = [
  #  path('users/',UserView.as_view()),
    re_path('(?P<version>[v1|v2]+)/users/', UserView.as_view(),name='api_user'),
    path('paser/',PaserView.as_view(),), #解析
    re_path('(?P<version>[v1|v2]+)/roles/', RolesView.as_view()), #序列化
]