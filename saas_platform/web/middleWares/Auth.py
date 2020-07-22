import datetime

from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from web import models


class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        '''如果用户登录'''
        user_id = request.session.get('user_id', 0)
        user_obj = models.Userinfo.objects.filter(id=user_id).first()
        request.user_obj = user_obj

        # 白名单 未登录都可访问的页面
        request_path_info = request.path_info
        if request_path_info in settings.WHILE_REGEX_URL_LIST:
            return None
        if not request.user_obj:
            return redirect("web:login")

        # 获取用户额度1
        object = models.Transaction.objects.filter(user=user_obj).order_by('-id').first()
        # 判断是否过期：
        current_datetime = datetime.datetime.now()
        if object.end_datetime and object.end_datetime < current_datetime:
            object = models.Transaction.objects.filter(user=user_obj, status=2, price_policy__category=1).first()
        request.price_policy = object.price_policy

        # 获取用户额度2
        # object = models.Transaction.objects.filter(user=user_obj).order_by('-id').first()
        # print('object = %s'%object)
        # if not object:
        #     request.price_policy = models.PricePolicy.objects.filter(category=1, title='免费版').first()
        #     # 没购买
        # else:
        #     current_datetime = datetime.datetime.now()
        #     if object.end_datetime  and object.end_datetime< current_datetime:
        #         request.price_policy = models.PricePolicy.objects.filter(category=1, title='免费版').first()
        #     else:
        #         request.price_policy = object.price_policy

    def process_view(self, request, view, args, kwargs):
        if not request.path_info.find('/manage/') !=-1:
            return

        project_id = kwargs.get('project_id')
        project_obj = models.Project.objects.filter(creator=request.user_obj, id=project_id).first()
        if project_obj:
            # 我创建的项目
            request.project = project_obj
            print('request.project = %s'%request.project)
            return

        project_user_obj = models.ProjectUser.objects.filter(user=request.user_obj, project_id=project_id).first()
        if project_user_obj:
            # 我参与的项目
            request.project = project_user_obj
            print('request.project = %s' % request.project)
            return
        return redirect('web:project_list')