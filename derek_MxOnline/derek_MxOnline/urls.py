"""derek_MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path, include
import xadmin

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView
from users.views import user_login, logout, register,forget_pwd
urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('users/', include('users.urls')),
    path('logout/',logout, name='logout'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('forget_pwd/', forget_pwd, name='forget_pwd'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

