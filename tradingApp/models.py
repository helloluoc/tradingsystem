from django.db import models

# Create your models here.
class User(models.Model):
    uname = models.CharField(max_length=20,unique=True,null=False,blank=False,verbose_name='用户名')
    upassword = models.CharField(verbose_name='密码',max_length=20,null=False)
    uicon = models.ImageField(verbose_name='用户头像')
    uremainder = models.FloatField(verbose_name="用户余额",default=1000)

class Good(models.Model):
    gname = models.CharField(verbose_name='货物名称',max_length=20)
    gprice = models.FloatField(verbose_name='货物价格')
    gclassify = models.CharField(max_length=20,verbose_name='货物分类')
    gtime = models.DateTimeField(verbose_name='添加时间',auto_now=True)
    gpicture = models.ImageField(default='/static/icon/1.jpg')
    #gbuyer = models.ManyToManyField(User)

class buyerCard(models.Model):
    cbuyer = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    cbuyerGoods = models.ManyToManyField(Good)
    cprice = models.FloatField(verbose_name='总价',default=0)
    cremainder = models.FloatField(verbose_name="用户余额",default=1000)


class comment(models.Model):
    guser = models.ForeignKey(Good)
    name = models.CharField(max_length=20,default='无名氏')
    contemt = models.TextField(max_length=250)
    datetime = models.DateTimeField(auto_now_add=True)

class cart(models.Model):
    goodId = models.ForeignKey(Good)
    useId = models.ForeignKey(User)
    gnumber = models.IntegerField(default=0)



