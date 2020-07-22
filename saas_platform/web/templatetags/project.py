from django.template import Library
from django.urls import reverse

from web import models

register = Library()
@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):
    # 1..获取我创建的所有项目
    my_project_list = models.Project.objects.filter(creator=request.user_obj)
    join_project_list = models.ProjectUser.objects.filter(user=request.user_obj)
    return {'my_project_list': my_project_list, 'join_project_list': join_project_list}

@register.inclusion_tag('inclusion/manage_menu_list.html')
def manage_menu_list(request):
    data_list = [
        {'title': '概览', 'url': reverse("web:dashboard", kwargs={"project_id": request.project.id})},
        {'title': '问题', 'url': reverse("web:issues", kwargs={"project_id": request.project.id})},
        {'title': '统计', 'url': reverse("web:statistics", kwargs={"project_id": request.project.id})},
        {'title': 'wiki', 'url': reverse("web:wiki", kwargs={"project_id": request.project.id})},
        {'title': '文件', 'url': reverse("web:file", kwargs={"project_id": request.project.id})},
        {'title': '配置', 'url': reverse("web:setting", kwargs={"project_id": request.project.id})},
    ]
    for item in data_list:
        print('request.path_info = %s'%str(request.path_info).split('/')[-2])
        print("item = %s"%str(item['url']).split('/')[-2])
        if (str(request.path_info).split('/')[-2]) == (str(item['url']).split('/')[-2]):
            print('--------------------')
            item['class'] = 'active'

    return {'data_list': data_list}
