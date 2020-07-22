from django import forms
from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection

from app01 import models


class RegisterModelForm(forms.ModelForm):
    # ret = re.match(r"^1[35678]\d{9}$", tel)
    # 重写字段,添加约束s
    mobile_phone = forms.CharField(label='手机号',
                                  validators=[RegexValidator(r"^1[35678]\d{9}$", "手机号格式错误"), ])
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码',
                                       widget=forms.PasswordInput(
                                           attrs={'class': "form-control",'placeholder':"请重复密码"}))
    vail_code = forms.CharField(label='验证码')
    class Meta:
        model = models.Userinfo
        fields = ['username', 'email','password', 'confirm_password', 'mobile_phone','vail_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{0}'.format(field.label)


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})


def getredisinfo(request):
    conn = get_redis_connection('default')
    conn.set('username', "rediszhansan", ex=20)
    val = conn.get('username')
    print(val)
    return HttpResponse(val)