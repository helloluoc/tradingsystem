# -*- coding: utf-8 -*-
"""
-------------------------------------------------
 File Name：  adminx
 Description :
 Author :  lc
 date：   7/23/18
-------------------------------------------------
"""
from extra_apps import xadmin
from .models import User

class userAdmin(object):
    pass

xadmin.site.register(User,userAdmin)