import datetime
import uuid

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from saas_platform import settings
from web import models
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    print(request.POST)
    form = RegisterModelForm(data=request.POST)
    print(form)
    if form.is_valid():
        # 验证通过，写入数据库
        # 用户表新建数据
        instance = form.save()
        # 创建交易记录 方式 1
        price_polocy = models.PricePolicy.objects.filter(category=1, title='免费版').first()
        models.Transaction.objects.create(
            status=2,
            order=str(uuid.uuid4()),
            user=instance,
            price_policy=price_polocy,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now()
        )
        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def send_sms(request):
    '''
    发送短信
    :param request:
    :return:
    '''
    print(request.GET.get("mobile_phone"))
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'errors': form.errors})


def login_sms(request):
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {'form': form})
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        # 用户输入正确，登录成功
        user_obj = form.cleaned_data['mobile_phone']
        print(user_obj)
        # 用户信息设置session
        request.session['user_id'] = user_obj.id
        request.session['user_name'] = user_obj.username
        request.session.set_expiry(60 * 60 * 24 * 14)  # session超时时间
        return JsonResponse({'status': True, 'data': "web/index/"})

    return JsonResponse({"status": False, "error": form.errors})


def login(request):
    '''用户名和密码登录'''
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.clean_passwrod()
        user_obj = models.Userinfo.objects.filter(Q(email=username) | Q(mobile_phone=username)).filter(
            password=password).first()
        if user_obj:
            request.session['user_id'] = user_obj.id
            request.session.set_expiry(60 * 60 * 24 * 14)  # session超时时间
            return redirect('web:index')
        form.add_error('username', '用户名或密码错误')
    return render(request, 'login.html', {'form': form})


def code_image(request):
    # 生成图片验证码
    from io import BytesIO
    from utils.ValiCode import check_code

    image_obj, valicode = check_code()
    request.session['vail_code'] = valicode  # 将验证码写入session
    request.session.set_expiry(60)  # session超时时间
    stream = BytesIO()
    image_obj.save(stream, 'png')

    return HttpResponse(stream.getvalue())
