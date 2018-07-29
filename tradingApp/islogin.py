# -*- coding: utf-8 -*-
"""
-------------------------------------------------
 File Name：  islogin
 Description :
 Author :  lc
 date：   7/28/18
-------------------------------------------------
"""
from django.http import HttpResponseRedirect

#如果登录则转到登录页面
def islogin(func):
    def login(request,*args,**kwargs):
        if request.session.get("username"):
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/login")
    return login