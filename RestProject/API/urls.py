from django.urls import path,re_path
from .views import UserView

urlpatterns = [
  #  path('users/',UserView.as_view()),
    re_path('(?P<version>[v1|v2]+)/users/', UserView.as_view())
]