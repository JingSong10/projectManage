import random

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from utils.encrypt import md5
from utils.tencent.sms import send_sms_single
from web import models
from web.forms.bootstrap import BootStrapForm


class RegisterModelForm(BootStrapForm, forms.ModelForm):
    # ret = re.match(r"^1[35678]\d{9}$", tel)
    # 重写字段,添加约束s
    mobile_phone = forms.CharField(label='手机号',
                                  validators=[RegexValidator(r"^1[35678]\d{9}$", "手机号格式错误"), ])

    password = forms.CharField(label='密码',widget=forms.PasswordInput(),
                               min_length=8,max_length=16,
                               error_messages={
                                   'min_length': "密码长度不能小于8位",
                                   'max_length': "密码长度不能大于16位"
                               })
    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput(),
                                       min_length=8, max_length=16,
                                       error_messages={
                                           'min_length': "密码长度不能小于8位",
                                           'max_length': "密码长度不能大于16位"}
                                       )

    vail_code = forms.CharField(label='验证码')

    class Meta:
        model = models.Userinfo
        fields = ['username', 'email','password', 'confirm_password', 'mobile_phone','vail_code']

    def clean_username(self):
        username = self.cleaned_data["username"]
        exists = models.Userinfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        exists = models.Userinfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return email

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        # 加密
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data["password"]
        confirm_password = md5(self.cleaned_data["confirm_password"])
        if pwd != confirm_password:
            raise ValidationError("两次输入的密码不一致")
        return confirm_password

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data["mobile_phone"]
        exists = models.Userinfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data["code"]
        mobile_phone = self.cleaned_data["mobile_phone"]
        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        print('redis_code = {0}'.format(redis_code))
        if not redis_code:
            raise ValidationError('验证码无效')
        redis_str_code = redis_code.decode('utf-8')
        if code.strip() != redis_str_code:
            raise ValidationError("验证码不正确， 请重新输入")


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['placeholder'] = '请输入{0}'.format(field.label)


class SendSmsForm(BootStrapForm, forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r"^1[35678]\d{9}$", "手机号格式错误"), ])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile_phone(self):

        '''手机号校验钩子'''
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.Userinfo.objects.filter(mobile_phone=mobile_phone).exists()

        # 短信模板校验
        template_id = self.request.GET.get('tpl')
        if not template_id:
            raise ValidationError('模板错误')


        tpl = self.request.GET.get('tpl')
        print('tpl = %s'%tpl)
        if tpl == 'login':
            if not exists:
                raise ValidationError('手机号不存在')
        else:
            if exists:
                raise ValidationError('手机号已存在')

        # 发短信
        code = random.randrange(1000, 9999)
        sms_result = send_sms_single(mobile_phone, template_id, [code, ])
        if sms_result['result'] != 0:
            raise ValidationError("短信发送失败, {0}".format(sms_result['errmsg']))
        # 验证码写入redis
        conn = get_redis_connection('default')
        print("写入的mobile_phone = %s"%mobile_phone)
        conn.set(mobile_phone, code, ex=60)
        return mobile_phone


class LoginSMSForm(BootStrapForm, forms.Form):
    mobile_phone = forms.CharField(label='手机号',
                                  validators=[RegexValidator(r"^1[35678]\d{9}$", "手机号格式错误"), ])

    vail_code = forms.CharField(label='验证码')

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data["mobile_phone"]
        user_obj = models.Userinfo.objects.filter(mobile_phone = mobile_phone).first()
        if not user_obj:
            raise ValidationError("手机号不存在")
        return user_obj

    def clean_vail_code(self):
        vail_code = self.cleaned_data['vail_code']
        user_obj = self.cleaned_data.get("mobile_phone")
        if not user_obj:
            # 手机号不存在,不校验
            return vail_code
        conn = get_redis_connection()
        redis_code = conn.get(user_obj.mobile_phone)
        print('redis_code = {0}'.format(redis_code))
        if not redis_code:
            raise ValidationError('验证码无效')
        redis_str_code = redis_code.decode('utf-8')
        if vail_code.strip() != redis_str_code:
            raise ValidationError("验证码不正确， 请重新输入")


class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='邮箱或手机号')
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True))
    vail_code = forms.CharField(label='图片验证码')

    def clean_vail_code(self):
        '''图片验证码'''
        vail_code = self.cleaned_data['vail_code']
        request_vail_code =self.request.session.get('vail_code')
        if not request_vail_code:
            raise ValidationError('验证码已过期，请重新获取')
        if vail_code.upper().strip() != request_vail_code.upper().strip():
            raise ValidationError('验证码输入错误')
        return vail_code

    def clean_passwrod(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
