from django.urls import path
from . import views

app_name='users'
urlpatterns =[
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/',views.logout,name='logout'),
    path('user/<int:pk>/profile/',views.profile, name='profile'),
    path('user/<int:pk>/profile/update/', views.profile_update, name='profile_update'),
    path('user/<int:pk>/pwdchange/', views.pwd_change, name="pwd_change"),
]