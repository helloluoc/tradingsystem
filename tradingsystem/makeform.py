'''
#因为django中的form中无法与Goods类相关联,所以还是不能用,单纯用在登录注册的地方还好
from django import forms

class commentForm(forms.Form):
    name = forms.CharField(max_length=20,label='姓名',error_messages={'required':'二蛋,姓名不能为空哦','invalid':'填写格式错误'})
    comment = forms.CharField(max_length=20,widget=forms.Textarea,label='评论',error_messages={'required':'狗剩你不是要写评论吗'})
    email = forms.CharField(max_length=30,label='邮件地址',error_messages={"required":'二楞写邮件地址啊'})

'''
