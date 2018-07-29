import io
import os
import random
import string

import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
#from tradingApp import models
from django.urls import reverse
from django.views.decorators.cache import cache_page

from tradingApp.islogin import islogin
from tradingApp.models import User,Good,comment,cart
from tradingsystem.settings import STATICFILES_DIRS, BASE_DIR

#注册
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        icon = request.FILES.get('icon')
        #vcode的原始数据由验证码生成函数保存在session里
        vcode = request.POST.get('vcode')
        print(vcode.lower())
        vcode_init = request.session.get('vcode')
        print(vcode_init.lower())
        if name and pwd and icon and (vcode.lower() == vcode_init.lower()):
            userifo = User()
            userifo.uname = name
            userifo.upassword = pwd

            # path = os.path.join(PTH_DIR,icon.name)
            # with open(path,'wb') as file:
            #     for buffer in icon.chunks():
            #         file.write(buffer)
            userifo.save()
            return HttpResponse('注册成功')
        else:
            vcode_init = request.session.get('vcode')
            print(vcode_init)
            return HttpResponse('注册失败')

#登录
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(uname=name)
        if (user.uname == name) and (user.upassword == password):
            request.session['username'] = user.uname
            return redirect(reverse(home,args='1'))
        else:
            return HttpResponse('登录失败')

@cache_page(60*2)
#首页展示,包含分页数据
def home(request, pagenum=1):
    time.sleep(10)
    loginUser = request.session.get("username")
    #如果登录成功则展示首页,否则跳回登录界面
    if loginUser:
        print(loginUser)
        goodAll = Good.objects.all()
        #构建分页器对象,每页展示2个对象
        paginator = Paginator(goodAll,5)
        #获取第n页的页面对象
        page = paginator.page(pagenum)
        data = {
            #当前页的对象列表
            'page': page,
            #分页页码范围
            'pagerange': paginator.page_range,
            #当前页的页码
            'currentpage':page.number,
        }
        return render(request,'home.html',context=data)
    else:
        print("*******************fuck***********************")
        return redirect("login")

#商品展示和购买页面
def readGoods(request,goodId):
    if request.session.get("username"):
        if request.method == 'GET':
            goodShow = Good.objects.get(id=goodId)
            comments = comment.objects.filter(guser_id=goodId).all()
            loginer = request.session.get('username')
            for i in comments:
                print(i.name)
            Goodlist = {
                'goods': goodShow,
                'comment': comments,
                'loginer': loginer,
            }
            return render(request, 'readgoods.html', context=Goodlist)
        else:
            #加入购物车
            buyer = request.session.get('username')
            print('顾客',buyer)
            buyerId = User.objects.get(uname=buyer).id
            goodShow = Good.objects.get(id=goodId).id
            num = request.POST.get('numberToBuy', 5)
            num = int(num)
            print("顾客ID:",buyerId,"货物ID:",goodShow)
            print('购买数量:')
            print(type(num))

            q = (Q(useId_id =buyerId ) & Q(goodId_id=goodShow))
            print('useid:',buyerId, "goodid:", goodShow)
            #同款商品之前被添加过,将两次次数相加
            try:
                buyer = cart.objects.get(Q(useId_id =buyerId ) & Q(goodId_id=goodShow))
                formerNum = buyer.gnumber
                buyer.gnumber = formerNum + num
                buyer.save()
            except:
                print(buyerId,'-----',goodShow)
                car = cart()
                car.useId_id = buyerId
                car.goodId_id = goodShow
                car.gnumber = num
                car.save()
            #评论
            comments = comment()
            comments.name = request.POST.get('name')
            comments.contemt = request.POST.get('comments')
            comments.guser_id = goodId
            comments.save()
            comments = comment.objects.filter(guser_id=goodId)
            Goodlist = {
                'goods': goodShow,
                'comment':comments,
                'username': request.session['username'],
            }
            return render(request,'readgoods.html',context=Goodlist)
    else:
        print("*******************fuck***********************")
        return redirect("login")

@islogin
def buyercar(request):
    if request.method == "GET":
        print("执行了测试程序")
        lguser = request.session.get("username")
        print(lguser)
        lguserId = User.objects.get(uname=lguser).id
        print("********" + str(lguserId))
        byGoods = cart.objects.filter(useId=lguserId)
        byGoods=list(byGoods)
        for i in range(len(byGoods)):
            list(byGoods[i])

        for i in byGoods:
            Id = i.goodId
            pricess = cart.objects.get(goodId=Id).goo

        byGood = {
            "buyered":byGoods,
        }
        return render(request, "buyercar.html", context=byGood)
        """
        #一个顾客购买的种类
        numBuy = cart.objects.filter(useId=lguserId).count()
        strs = ""
        for i in range(numBuy+1):
            strs = strs + "s"
        shit = {}
        shit["num"] = strs
        """




#验证码生成函数
def getvcode(request):

    # 随机生成验证码
    population = string.ascii_letters+string.digits
    letterlist = random.sample(population,4)
    vcode = ''.join(letterlist)

    # 保存该用户的验证码
    request.session['vcode']=vcode
    print('init:'+vcode)

    # 绘制验证码
    # 需要画布
    image = Image.new('RGB',(176,50),color=getRandomColor())
    # 创建画布的画笔
    draw = ImageDraw.Draw(image)
    # 绘制文字
    path = os.path.join(BASE_DIR,'static','TakaoPGothic.ttf')
    font = ImageFont.truetype(path,50)

    for i in range(len(vcode)):
        draw.text((20+40*i,0),vcode[i],fill=getRandomColor(),font=font)

    # 添加噪声
    for i in range(500):
        position = (random.randint(0,176),random.randint(0,50))
        draw.point(position,fill=getRandomColor())

    # 返回验证码字节数据
    # 创建字节容器
    buffer = io.BytesIO()
    # 将画布内容丢入容器
    image.save(buffer,'png')
    # 返回容器内的字节

    return HttpResponse(buffer.getvalue(),'image/png')


def getRandomColor():
    red = random.randint(0,256)
    green = random.randint(0,256)
    blue = random.randint(0,256)
    return (red,green,blue)


