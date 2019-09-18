from django.urls import path

from . import views

app_name='users'

urlpatterns =[
    path('profile/', views.user_info, name='user_info'),
    path('logout/',views.logout, name='logout'),
    path('modify_pwd/',views.ModifyPwdView.as_view(), name='modify_pwd'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('active/<str:active_code>/', views.ActiveUserView.as_view(), name='user_active'),
    path('reset/<str:active_code>/', views.ResetView.as_view(), name='reset_pwd'),
    path('forget_pwd/', views.ForgetPwdView.as_view(), name='forget_pwd'),

   #个人中心
    path("users/info/", views.UserInfoView.as_view(), name='user_info'),
    path('users/image/upload', views.UploadImageView.as_view(), name='image_upload'),
    path("users/update/pwd/",views.UpdatePwdView.as_view(), name='update_pwd'),
    path('users/sendemail_code/', views.SendEmailCodeView.as_view(), name='sendemail_code'),
    path("users/update_email/", views.UpdateEmailView.as_view(),name='update_email'),
]