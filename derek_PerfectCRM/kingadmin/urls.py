from django.urls import path
from kingadmin import views

urlpatterns =[
 # kingadmin 的单独登录后台
 path('login/', views.acc_login, name='login'),
 path('logout/', views.acc_logout, name='logout'),

 path('', views.app_index, name='app_index'),
 path('<str:app_name>/<str:model_name>/', views.table_obj_list, name='table_obj_list'),
 path('<str:app_name>/<str:model_name>/<int:pk>/change/', views.table_obj_change, name='table_obj_change'),
 path('<str:app_name>/<str:model_name>/add/', views.table_obj_add, name='table_obj_add'),
]