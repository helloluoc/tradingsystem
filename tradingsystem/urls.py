"""tradingsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import social_django

from django.conf.urls import url
from django.contrib import admin

from extra_apps import xadmin
from tradingApp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register',views.register,name='register'),
    url(r'^login',views.login,name='login'),
    url(r'home/(\d+)/',views.home,name='home'),
    url(r'^getvcode',views.getvcode,name='fuck'),
    url(r'^goodlist/(\d+)/',views.readGoods,name='goodlist'),
    url(r"^fuck",xadmin.site.urls),
    url(r"^bcar",views.buyercar,name="buyercar")
    #url(r'^test/',views.test,name='test'),
    #url('',social_django.urls, namespace='social'),
]
