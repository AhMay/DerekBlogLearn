from django.urls import path
from crm import views

app_name='crm'

urlpatterns =[
    path('', views.dashboard),
    path('login/', views.acc_login),
    path('logout/', views.acc_logout, name='logout')
]